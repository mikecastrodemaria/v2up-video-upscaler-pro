"""
Model Downloader - Automatic download of AI model weights
Downloads models from Hugging Face or GitHub releases
"""

import os
import urllib.request
import hashlib
from pathlib import Path
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)


# Model URLs and checksums
MODEL_URLS = {
    'realesrgan_x4plus': {
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
        'filename': 'RealESRGAN_x4plus.pth',
        'md5': '4fa0d38905f75ac06eb49a7951b426670',  # Example, update with actual
    },
    'realesrgan_x2plus': {
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
        'filename': 'RealESRGAN_x2plus.pth',
        'md5': None,
    },
    'realesrgan_x4plus_anime': {
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth',
        'filename': 'RealESRGAN_x4plus_anime_6B.pth',
        'md5': None,
    },
}


def get_model_dir() -> Path:
    """
    Get the directory for storing model weights

    Returns:
        Path: Model directory path
    """
    # Try to get from environment variable first
    model_dir = os.environ.get('VIDEO_UPSCALER_MODEL_DIR')

    if model_dir:
        model_path = Path(model_dir)
    else:
        # Default to ~/.cache/video-upscaler-pro/models
        if os.name == 'nt':  # Windows
            cache_dir = Path(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')))
        else:  # Linux/macOS
            cache_dir = Path.home() / '.cache'

        model_path = cache_dir / 'video-upscaler-pro' / 'models'

    # Create directory if it doesn't exist
    model_path.mkdir(parents=True, exist_ok=True)

    return model_path


def download_file(
    url: str,
    output_path: Path,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> bool:
    """
    Download file from URL with progress tracking

    Args:
        url: URL to download from
        output_path: Output file path
        progress_callback: Optional callback(downloaded_bytes, total_bytes)

    Returns:
        bool: True if successful
    """
    try:
        logger.info(f"Downloading from {url}")

        # Create a custom progress hook
        def reporthook(block_num, block_size, total_size):
            if progress_callback:
                downloaded = block_num * block_size
                progress_callback(downloaded, total_size)

        # Download file
        urllib.request.urlretrieve(url, output_path, reporthook=reporthook)

        logger.info(f"Downloaded to {output_path}")
        return True

    except Exception as e:
        logger.error(f"Download failed: {e}")
        if output_path.exists():
            output_path.unlink()  # Remove partial download
        return False


def verify_file_md5(file_path: Path, expected_md5: str) -> bool:
    """
    Verify file MD5 checksum

    Args:
        file_path: Path to file
        expected_md5: Expected MD5 hash

    Returns:
        bool: True if matches
    """
    try:
        md5_hash = hashlib.md5()

        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)

        actual_md5 = md5_hash.hexdigest()
        return actual_md5 == expected_md5

    except Exception as e:
        logger.error(f"MD5 verification failed: {e}")
        return False


def download_model(
    model_name: str,
    force_download: bool = False,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> Optional[Path]:
    """
    Download model weights if not already present

    Args:
        model_name: Model name (e.g., 'realesrgan_x4plus')
        force_download: Force re-download even if file exists
        progress_callback: Optional progress callback

    Returns:
        Path: Path to model file, or None if failed
    """
    if model_name not in MODEL_URLS:
        logger.error(f"Unknown model: {model_name}")
        logger.info(f"Available models: {list(MODEL_URLS.keys())}")
        return None

    model_info = MODEL_URLS[model_name]
    model_dir = get_model_dir()
    model_path = model_dir / model_info['filename']

    # Check if already downloaded
    if model_path.exists() and not force_download:
        logger.info(f"Model already exists: {model_path}")

        # Verify MD5 if provided
        if model_info.get('md5'):
            if verify_file_md5(model_path, model_info['md5']):
                return model_path
            else:
                logger.warning("MD5 mismatch, re-downloading...")
        else:
            return model_path

    # Download model
    logger.info(f"Downloading model: {model_name}")

    success = download_file(model_info['url'], model_path, progress_callback)

    if success:
        # Verify MD5 if provided
        if model_info.get('md5'):
            if verify_file_md5(model_path, model_info['md5']):
                logger.info("MD5 verification passed")
                return model_path
            else:
                logger.error("MD5 verification failed")
                model_path.unlink()
                return None
        return model_path
    else:
        return None


def list_available_models() -> list:
    """
    List all available models

    Returns:
        list: List of model names
    """
    return list(MODEL_URLS.keys())


def list_downloaded_models() -> list:
    """
    List all downloaded models

    Returns:
        list: List of model names that are downloaded
    """
    model_dir = get_model_dir()
    downloaded = []

    for model_name, info in MODEL_URLS.items():
        model_path = model_dir / info['filename']
        if model_path.exists():
            downloaded.append(model_name)

    return downloaded


def get_model_path(model_name: str) -> Optional[Path]:
    """
    Get path to model file (downloads if necessary)

    Args:
        model_name: Model name

    Returns:
        Path: Path to model file, or None if not available
    """
    return download_model(model_name)


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes to human-readable string

    Args:
        bytes_size: Size in bytes

    Returns:
        str: Formatted size (e.g., "10.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"
