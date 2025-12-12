"""
Spatial Upscaler - Video upscaling with AI models
Handles upscaling of entire videos frame-by-frame
"""

import time
import os
from typing import Dict, Optional, Callable
from pathlib import Path
import logging

from models.realesrgan_model import create_realesrgan_model
from utils.video_processor import VideoProcessor, VideoWriter
from utils.system_manager import get_system_manager

logger = logging.getLogger(__name__)


class SpatialUpscaler:
    """
    Handles spatial upscaling of videos using AI models
    """

    def __init__(
        self,
        model_name: str = 'realesrgan',
        scale_factor: float = 4.0,
        device: str = 'auto'
    ):
        """
        Initialize spatial upscaler

        Args:
            model_name: Model to use ('realesrgan', 'swinir', 'seedvr2')
            scale_factor: Scaling factor (0.1 to 16.0)
                         - Values >= 1.0: Upscaling
                         - Values < 1.0: Downscaling
                         - 2.0, 4.0: Optimal (pure AI)
                         - Other values: Hybrid (AI + resize)
            device: 'cuda', 'cpu', or 'auto'
        """
        self.model_name = model_name
        self.scale_factor = float(scale_factor)

        # Get system manager
        self.sys_manager = get_system_manager()

        # Determine device
        if device == 'auto':
            device = self.sys_manager.get_device()

        self.device = device

        # Validate scale factor
        if self.scale_factor <= 0 or self.scale_factor > 16.0:
            raise ValueError(f"Invalid scale factor: {scale_factor}. Must be between 0.1 and 16.0.")

        # Initialize model (only if upscaling with AI)
        self.model = None
        self.use_ai = self.scale_factor >= 1.5  # Use AI for scales >= 1.5x
        if self.use_ai:
            self._load_model()

    def _load_model(self):
        """Load the AI model"""
        # Determine optimal AI model scale based on target scale
        if self.scale_factor >= 3.0:
            self.ai_model_scale = 4
            logger.info(f"Using 4× AI model for {self.scale_factor}× target scale")
        else:  # 1.5 <= scale < 3.0
            self.ai_model_scale = 2
            logger.info(f"Using 2× AI model for {self.scale_factor}× target scale")

        logger.info(f"Loading {self.model_name} model (AI scale={self.ai_model_scale}, target={self.scale_factor}, device={self.device})")

        try:
            if self.model_name.lower() == 'realesrgan':
                # Get optimal settings
                settings = self.sys_manager.optimal_settings

                self.model = create_realesrgan_model(
                    scale=self.ai_model_scale,
                    device=self.device,
                    fp16=settings['use_fp16'],
                    tile_size=settings.get('tile_size', 0)
                )

                logger.info(f"Real-ESRGAN {self.ai_model_scale}× model loaded successfully")

            else:
                raise NotImplementedError(f"Model {self.model_name} not yet implemented")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def upscale_video(
        self,
        input_path: str,
        output_path: str,
        start_frame: int = 0,
        end_frame: Optional[int] = None,
        progress_callback: Optional[Callable[[int, int, float], None]] = None
    ) -> Dict:
        """
        Upscale a video

        Args:
            input_path: Input video path
            output_path: Output video path
            start_frame: Starting frame index
            end_frame: Ending frame index (None = all frames)
            progress_callback: Optional callback(current_frame, total_frames, eta)

        Returns:
            dict: Processing results with 'success', 'output_path', 'metrics'
        """
        logger.info(f"Starting video upscaling: {input_path}")
        logger.info(f"Output: {output_path}")
        logger.info(f"Scale: {self.scale_factor}x, Model: {self.model_name}")

        start_time = time.time()

        try:
            # Open input video
            with VideoProcessor(input_path) as vp:
                metadata = vp.get_metadata()

                logger.info(f"Input resolution: {metadata['width']}x{metadata['height']}")
                logger.info(f"FPS: {metadata['fps']}, Frames: {metadata['frame_count']}")

                # Calculate output resolution (convert to int for OpenCV)
                output_width = int(metadata['width'] * self.scale_factor)
                output_height = int(metadata['height'] * self.scale_factor)

                logger.info(f"Output resolution: {output_width}x{output_height}")

                # Validate output resolution (check total megapixels, not individual dimensions)
                # This allows portrait videos to have height > 4320 if total pixels < 8K
                output_megapixels = (output_width * output_height) / (1024 * 1024)
                max_megapixels = 33.2  # 8K = 7680x4320 = 33.2 MP

                if output_megapixels > max_megapixels:
                    raise ValueError(
                        f"Output resolution ({output_width}x{output_height}, {output_megapixels:.1f}MP) "
                        f"exceeds 8K limit ({max_megapixels}MP)"
                    )

                logger.info(f"Output: {output_megapixels:.1f} MP (limit: {max_megapixels} MP)")

                # Determine frame range
                if end_frame is None:
                    end_frame = metadata['frame_count']

                total_frames = end_frame - start_frame
                logger.info(f"Processing {total_frames} frames")

                # Check VRAM if using GPU
                if self.device == 'cuda':
                    estimated_vram = self.model.estimate_vram_usage((metadata['width'], metadata['height']))
                    sufficient, msg = self.sys_manager.check_vram_requirement(estimated_vram)
                    logger.info(msg)

                    if not sufficient:
                        logger.warning("Insufficient VRAM, but will try anyway...")

                # Open output video writer
                with VideoWriter(
                    output_path,
                    fps=metadata['fps'],
                    resolution=(output_width, output_height),
                    audio_source=input_path
                ) as writer:

                    # Process frames
                    processed_count = 0
                    frame_times = []

                    for frame_idx, frame in vp.extract_frames(start_frame, end_frame):
                        frame_start = time.time()

                        # Upscale frame
                        upscaled = self._upscale_frame(frame)

                        # Write frame
                        writer.write_frame(upscaled)

                        processed_count += 1
                        frame_time = time.time() - frame_start
                        frame_times.append(frame_time)

                        # Calculate ETA
                        if len(frame_times) > 0:
                            avg_time = sum(frame_times[-30:]) / min(len(frame_times), 30)  # Rolling average
                            remaining_frames = total_frames - processed_count
                            eta = remaining_frames * avg_time
                        else:
                            eta = 0

                        # Progress callback
                        if progress_callback and processed_count % 10 == 0:
                            progress_callback(processed_count, total_frames, eta)

                        # Log progress
                        if processed_count % 100 == 0:
                            logger.info(f"Processed {processed_count}/{total_frames} frames ({processed_count/total_frames*100:.1f}%)")

                        # Clear cache periodically
                        if processed_count % 50 == 0:
                            self.model.clear_cache()

            # Calculate metrics
            total_time = time.time() - start_time

            logger.info(f"Video upscaling completed in {total_time:.2f}s")
            logger.info(f"Average: {total_time/total_frames:.3f}s per frame")

            return {
                'success': True,
                'output_path': output_path,
                'metrics': {
                    'total_time': total_time,
                    'frames_processed': processed_count,
                    'avg_time_per_frame': total_time / processed_count if processed_count > 0 else 0,
                    'input_resolution': f"{metadata['width']}x{metadata['height']}",
                    'output_resolution': f"{output_width}x{output_height}",
                    'scale_factor': self.scale_factor
                }
            }

        except Exception as e:
            logger.error(f"Error during video upscaling: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'output_path': None,
                'metrics': {}
            }

    def _upscale_frame(self, frame):
        """
        Upscale a single frame with arbitrary scale factor

        Args:
            frame: Input frame (numpy array, BGR)

        Returns:
            numpy.ndarray: Upscaled/downscaled frame
        """
        import cv2

        original_h, original_w = frame.shape[:2]
        target_h = int(original_h * self.scale_factor)
        target_w = int(original_w * self.scale_factor)

        # Case 1: Downscaling (< 1.0) - use high-quality Lanczos
        if self.scale_factor < 1.0:
            return cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

        # Case 2: Small upscaling (< 1.5) - use traditional resize
        elif self.scale_factor < 1.5:
            return cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

        # Case 3: Exact AI match (2.0 or 4.0) - use AI directly
        elif self.scale_factor == 2.0:
            return self.model.upscale_image(frame)

        elif self.scale_factor == 4.0:
            return self.model.upscale_image(frame)

        # Case 4: Large scale (8.0+) - apply 4× AI multiple times
        elif self.scale_factor >= 8.0:
            # Apply 4× AI repeatedly
            times = int(self.scale_factor / 4)
            for _ in range(times):
                frame = self.model.upscale_image(frame)

            # Handle remainder with resize
            remainder = self.scale_factor / (4 ** times)
            if abs(remainder - 1.0) > 0.01:  # Not exact
                current_h, current_w = frame.shape[:2]
                final_h = int(current_h * remainder)
                final_w = int(current_w * remainder)
                frame = cv2.resize(frame, (final_w, final_h), interpolation=cv2.INTER_LANCZOS4)

            return frame

        # Case 5: Arbitrary scale - hybrid approach (AI + resize)
        else:
            # Use AI upscaling first
            frame = self.model.upscale_image(frame)

            # Then resize to exact target
            ai_scaled_h, ai_scaled_w = frame.shape[:2]
            resize_factor = self.scale_factor / self.ai_model_scale

            final_h = int(original_h * self.scale_factor)
            final_w = int(original_w * self.scale_factor)

            if abs(resize_factor - 1.0) > 0.01:  # Need resize
                frame = cv2.resize(frame, (final_w, final_h), interpolation=cv2.INTER_LANCZOS4)

            return frame

    def upscale_preview(
        self,
        input_path: str,
        output_path: str,
        duration: float = 5.0,
        progress_callback: Optional[Callable[[int, int, float], None]] = None
    ) -> Dict:
        """
        Upscale first N seconds for preview

        Args:
            input_path: Input video path
            output_path: Output video path
            duration: Duration in seconds to process
            progress_callback: Optional progress callback

        Returns:
            dict: Processing results
        """
        logger.info(f"Creating preview ({duration}s) of {input_path}")

        try:
            # Get video metadata
            with VideoProcessor(input_path) as vp:
                metadata = vp.get_metadata()
                fps = metadata['fps']

                # Calculate frame range
                end_frame = min(int(fps * duration), metadata['frame_count'])

            # Upscale the segment
            return self.upscale_video(
                input_path,
                output_path,
                start_frame=0,
                end_frame=end_frame,
                progress_callback=progress_callback
            )

        except Exception as e:
            logger.error(f"Error creating preview: {e}")
            return {
                'success': False,
                'error': str(e),
                'output_path': None,
                'metrics': {}
            }

    def estimate_processing_time(self, input_path: str) -> Dict:
        """
        Estimate processing time for a video

        Args:
            input_path: Input video path

        Returns:
            dict: Estimated times
        """
        try:
            with VideoProcessor(input_path) as vp:
                metadata = vp.get_metadata()

            # Rough estimates based on hardware
            if self.device == 'cuda':
                vram = self.sys_manager.device_info['vram_total_gb']

                if vram >= 12:
                    time_per_frame = 0.05  # RTX 4090, etc.
                elif vram >= 8:
                    time_per_frame = 0.15  # RTX 3060, etc.
                elif vram >= 6:
                    time_per_frame = 0.3   # RTX 3050, etc.
                else:
                    time_per_frame = 0.5   # Entry level
            else:
                time_per_frame = 3.0  # CPU is much slower

            # Adjust for scale factor
            time_per_frame *= (self.scale_factor / 4.0)

            total_time = time_per_frame * metadata['frame_count']

            return {
                'total_frames': metadata['frame_count'],
                'estimated_time_per_frame': time_per_frame,
                'estimated_total_time': total_time,
                'estimated_total_time_formatted': self._format_time(total_time)
            }

        except Exception as e:
            logger.error(f"Error estimating time: {e}")
            return {
                'error': str(e)
            }

    def _format_time(self, seconds: float) -> str:
        """Format seconds as HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"


def create_upscaler(
    model_name: str = 'realesrgan',
    scale_factor: int = 4,
    device: str = 'auto'
) -> SpatialUpscaler:
    """
    Factory function to create upscaler

    Args:
        model_name: Model name
        scale_factor: Scale factor (2, 4, 8)
        device: Device ('cuda', 'cpu', 'auto')

    Returns:
        SpatialUpscaler: Initialized upscaler
    """
    return SpatialUpscaler(
        model_name=model_name,
        scale_factor=scale_factor,
        device=device
    )
