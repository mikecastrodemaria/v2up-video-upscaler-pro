"""
Test script to verify model download works correctly
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.model_downloader import download_model, get_model_dir

def test_model_download():
    """Test downloading the RealESRGAN model"""
    print("=" * 60)
    print("Testing RealESRGAN Model Download")
    print("=" * 60)
    print()

    # Show model directory
    model_dir = get_model_dir()
    print(f"Model directory: {model_dir}")
    print()

    # Try to download the model
    print("Downloading realesrgan_x4plus model...")
    model_path = download_model('realesrgan_x4plus')

    if model_path:
        print()
        print("=" * 60)
        print("SUCCESS: Model downloaded successfully!")
        print("=" * 60)
        print(f"Model path: {model_path}")
        print(f"File size: {model_path.stat().st_size / (1024**2):.1f} MB")
        return True
    else:
        print()
        print("=" * 60)
        print("FAILED: Model download failed")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_model_download()
    sys.exit(0 if success else 1)
