"""
Test script to verify RealESRGAN model can be loaded and used
"""

import sys
import logging
import numpy as np
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from models.realesrgan_model import create_realesrgan_model
    print("=" * 60)
    print("Testing RealESRGAN Model Loading")
    print("=" * 60)
    print()

    # Determine device
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    if device == 'cuda':
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")
    print()

    # Create model
    print("Loading RealESRGAN model...")
    model = create_realesrgan_model(
        scale=4,
        device=device,
        fp16=True if device == 'cuda' else False,
        tile_size=256  # Use smaller tile for testing
    )
    print("Model loaded successfully!")
    print()

    # Create a test image (small 100x100)
    print("Testing with a small 100x100 test image...")
    test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    # Upscale
    print("Upscaling test image...")
    output = model.upscale_image(test_image)

    print(f"Input shape: {test_image.shape}")
    print(f"Output shape: {output.shape}")
    print()

    # Verify output
    expected_height = test_image.shape[0] * 4
    expected_width = test_image.shape[1] * 4

    if output.shape[0] == expected_height and output.shape[1] == expected_width:
        print("=" * 60)
        print("SUCCESS: Model works correctly!")
        print("=" * 60)
        print(f"Upscaled from {test_image.shape} to {output.shape}")
        sys.exit(0)
    else:
        print("=" * 60)
        print("ERROR: Output dimensions are incorrect")
        print("=" * 60)
        sys.exit(1)

except Exception as e:
    print()
    print("=" * 60)
    print(f"ERROR: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
