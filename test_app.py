#!/usr/bin/env python3
"""
Test Script for Video Upscaler Pro
Generates test videos and provides easy testing interface
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("Video Upscaler Pro - Testing Utility")
    print("=" * 60)
    print()

    # Check dependencies
    print("[1/4] Checking dependencies...")
    try:
        import gradio
        import torch
        import cv2
        import numpy
        print("✓ All dependencies installed")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease run the installation script:")
        print("  Windows: install.bat")
        print("  Linux/macOS: ./install.sh")
        return 1

    # Generate test videos
    print("\n[2/4] Generating test videos...")
    from tests.test_video_generator import TestVideoGenerator

    test_dir = Path("test_videos")
    generator = TestVideoGenerator(str(test_dir))

    try:
        # Generate a quick test video (small and fast)
        print("  Creating test video (640x480, 5 seconds)...")
        videos = {
            'moving_shapes': generator.generate_moving_shapes(
                resolution=(640, 480),
                fps=30.0,
                duration=5.0
            )
        }

        print(f"✓ Test videos created in: {test_dir}")
        print(f"  - moving_shapes.mp4")

    except Exception as e:
        print(f"✗ Error generating test videos: {e}")
        print("  Continuing anyway...")

    # Test system detection
    print("\n[3/4] Testing system detection...")
    try:
        from utils.system_manager import get_system_manager

        sys_manager = get_system_manager()
        info = sys_manager.device_info

        print(f"  Platform: {info['platform']}")
        print(f"  Device: {info['device_name']}")

        if info['has_cuda']:
            print(f"  CUDA: Available")
            print(f"  VRAM: {info['vram_available_gb']:.1f} GB / {info['vram_total_gb']:.1f} GB")
        else:
            print(f"  CUDA: Not available (CPU mode)")

        print(f"  CPU Cores: {info['cpu_count']}")
        print(f"  RAM: {info['ram_total_gb']:.1f} GB")

        print("✓ System detection working")

    except Exception as e:
        print(f"✗ Error in system detection: {e}")

    # Start application
    print("\n[4/4] Starting application...")
    print()
    print("=" * 60)
    print("Application will open in your browser")
    print("=" * 60)
    print()
    print("Quick Test Guide:")
    print("  1. Upload test_videos/moving_shapes.mp4")
    print("  2. Try 2x upscaling first (faster)")
    print("  3. Click 'Preview' to test first 5 seconds")
    print("  4. Try enabling FPS Interpolation")
    print("  5. Check the System tab for hardware info")
    print()
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    print()

    try:
        from ui.gradio_app import create_interface

        app = create_interface()
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=True,
            show_error=True
        )

    except KeyboardInterrupt:
        print("\n\nShutting down...")
        return 0

    except Exception as e:
        print(f"\n✗ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
