"""
Real-ESRGAN Model Wrapper
Wrapper for Real-ESRGAN super-resolution model
"""

import torch
import numpy as np
import cv2
from typing import Optional, Union
import logging

try:
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
    REALESRGAN_AVAILABLE = True
except ImportError:
    REALESRGAN_AVAILABLE = False
    logging.warning("Real-ESRGAN not available. Please install: pip install realesrgan basicsr")

from utils.model_downloader import download_model

logger = logging.getLogger(__name__)


class RealESRGANModel:
    """Real-ESRGAN model wrapper"""

    def __init__(
        self,
        scale: int = 4,
        model_name: str = 'realesrgan_x4plus',
        device: str = 'cuda',
        tile_size: int = 0,
        tile_pad: int = 10,
        pre_pad: int = 0,
        fp16: bool = False
    ):
        """
        Initialize Real-ESRGAN model

        Args:
            scale: Upscaling factor (2, 4)
            model_name: Model variant name
            device: 'cuda' or 'cpu'
            tile_size: Tile size for processing (0 = no tiling)
            tile_pad: Padding for tiles
            pre_pad: Pre-padding for input
            fp16: Use FP16 (half precision)
        """
        if not REALESRGAN_AVAILABLE:
            raise ImportError("Real-ESRGAN not available. Please install required packages.")

        self.scale = scale
        self.model_name = model_name
        self.device = device
        self.tile_size = tile_size
        self.fp16 = fp16

        # Download model if needed
        logger.info(f"Loading Real-ESRGAN model: {model_name}")
        model_path = download_model(model_name)

        if model_path is None:
            raise RuntimeError(f"Failed to download model: {model_name}")

        # Determine model architecture
        if 'anime' in model_name:
            num_block = 6
            num_feat = 64
        else:
            num_block = 23
            num_feat = 64

        # Create model
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=num_feat,
            num_block=num_block,
            num_grow_ch=32,
            scale=scale
        )

        # Initialize upsampler
        try:
            self.upsampler = RealESRGANer(
                scale=scale,
                model_path=str(model_path),
                model=model,
                tile=tile_size,
                tile_pad=tile_pad,
                pre_pad=pre_pad,
                half=fp16,
                device=device
            )
            logger.info(f"Real-ESRGAN model loaded successfully on {device}")

        except (torch.cuda.CudaError, RuntimeError) as e:
            if device == 'cuda' and 'cudaErrorNoKernelImageForDevice' in str(e):
                # RTX 5090 or newer GPU not fully supported, fall back to CPU
                logger.warning(f"CUDA kernel not available for this GPU, falling back to CPU")
                logger.warning("Your GPU may be too new for this PyTorch version")

                self.device = 'cpu'
                self.upsampler = RealESRGANer(
                    scale=scale,
                    model_path=str(model_path),
                    model=model,
                    tile=tile_size,
                    tile_pad=tile_pad,
                    pre_pad=pre_pad,
                    half=False,  # CPU doesn't support half precision
                    device='cpu'
                )
                logger.info(f"Real-ESRGAN model loaded successfully on CPU (fallback mode)")
            else:
                raise

    def upscale_image(
        self,
        image: np.ndarray,
        outscale: Optional[float] = None
    ) -> np.ndarray:
        """
        Upscale a single image

        Args:
            image: Input image (BGR format, numpy array)
            outscale: Output scale (None = use model scale)

        Returns:
            numpy.ndarray: Upscaled image (BGR format)
        """
        try:
            # Ensure image is in correct format
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)

            # Upscale using Real-ESRGAN
            output, _ = self.upsampler.enhance(image, outscale=outscale)

            return output

        except Exception as e:
            logger.error(f"Error upscaling image: {e}")
            # Fallback to simple resize
            if outscale is None:
                outscale = self.scale
            h, w = image.shape[:2]
            return cv2.resize(
                image,
                (int(w * outscale), int(h * outscale)),
                interpolation=cv2.INTER_LANCZOS4
            )

    def upscale_image_pil(self, pil_image):
        """
        Upscale PIL Image

        Args:
            pil_image: PIL Image

        Returns:
            PIL Image: Upscaled image
        """
        from PIL import Image

        # Convert PIL to numpy (RGB -> BGR)
        img_np = np.array(pil_image)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Upscale
        output_bgr = self.upscale_image(img_bgr)

        # Convert back to RGB
        output_rgb = cv2.cvtColor(output_bgr, cv2.COLOR_BGR2RGB)

        return Image.fromarray(output_rgb)

    def estimate_vram_usage(self, input_resolution: tuple) -> float:
        """
        Estimate VRAM usage in GB

        Args:
            input_resolution: (width, height)

        Returns:
            float: Estimated VRAM in GB
        """
        width, height = input_resolution
        pixels = width * height

        # Rough estimation based on experiments
        # Base model: ~2GB, additional per megapixel
        base_usage = 2.0
        per_megapixel = 0.5 if self.fp16 else 1.0

        megapixels = pixels / (1024 * 1024)
        estimated = base_usage + (megapixels * per_megapixel * self.scale * self.scale)

        return estimated

    def get_optimal_tile_size(self, vram_gb: float) -> int:
        """
        Get optimal tile size based on available VRAM

        Args:
            vram_gb: Available VRAM in GB

        Returns:
            int: Optimal tile size
        """
        if vram_gb >= 12:
            return 512
        elif vram_gb >= 8:
            return 384
        elif vram_gb >= 6:
            return 256
        elif vram_gb >= 4:
            return 192
        else:
            return 128

    def clear_cache(self):
        """Clear CUDA cache"""
        if self.device == 'cuda' and torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()


def create_realesrgan_model(
    scale: int = 4,
    device: str = 'cuda',
    fp16: bool = True,
    tile_size: int = 0
) -> RealESRGANModel:
    """
    Factory function to create Real-ESRGAN model

    Args:
        scale: Upscaling factor (2, 4)
        device: 'cuda' or 'cpu'
        fp16: Use half precision
        tile_size: Tile size (0 = auto)

    Returns:
        RealESRGANModel: Initialized model
    """
    # Select model based on scale
    if scale == 2:
        model_name = 'realesrgan_x2plus'
    elif scale == 4:
        model_name = 'realesrgan_x4plus'
    else:
        raise ValueError(f"Unsupported scale: {scale}. Use 2 or 4.")

    # Auto-determine tile size if needed
    if tile_size == 0 and device == 'cuda':
        try:
            import torch
            if torch.cuda.is_available():
                vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                if vram_gb < 8:
                    tile_size = 256
        except:
            pass

    return RealESRGANModel(
        scale=scale,
        model_name=model_name,
        device=device,
        tile_size=tile_size,
        fp16=fp16
    )
