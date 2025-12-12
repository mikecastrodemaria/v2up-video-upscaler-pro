#!/usr/bin/env python3
"""
Video Upscaler Pro - Main Application Entry Point
Open source video upscaling application using AI models
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import gradio
        import torch
        import cv2
        import numpy
        return True
    except ImportError as e:
        print(f"ERROR: Missing required dependency: {e}")
        print("\nPlease run the installation script:")
        print("  Windows: install.bat")
        print("  Linux/macOS: ./install.sh")
        return False

def main():
    """Main application entry point"""
    print("=" * 50)
    print("Video Upscaler Pro - Starting...")
    print("=" * 50)
    print()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Import UI module
    try:
        from ui.gradio_app import create_interface
    except ImportError as e:
        print(f"ERROR: Failed to import UI module: {e}")
        print("\nThe application may not be properly installed.")
        sys.exit(1)

    # Create and launch the interface
    try:
        print("Creating Gradio interface...")
        app = create_interface()

        print()
        print("=" * 50)
        print("Application is ready!")
        print("=" * 50)
        print()
        print("Opening in your browser...")
        print("If it doesn't open automatically, visit: http://localhost:7860")
        print()
        print("Press Ctrl+C to stop the application")
        print()

        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=True,
            show_error=True
        )
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
