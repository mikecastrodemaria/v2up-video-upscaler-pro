# Python 3.13 Workaround Guide

## Issue

Python 3.13 has compatibility issues with BasicSR and Real-ESRGAN packages due to changes in the build system. This causes installation failures.

## Recommended Solution

**Use Python 3.10, 3.11, or 3.12** for the best experience.

Download Python 3.12: https://www.python.org/downloads/release/python-3120/

## Alternative: Manual Installation for Python 3.13

If you must use Python 3.13, follow these steps:

### Step 1: Install Core Dependencies

```bash
# Install basic requirements first
pip install gradio torch torchvision opencv-python pillow
pip install imageio-ffmpeg moviepy psutil tqdm pyyaml scikit-image
```

### Step 2: Install BasicSR Manually

```bash
# Clone BasicSR with a specific commit that works better
git clone https://github.com/XPixelGroup/BasicSR.git temp_basicsr
cd temp_basicsr

# Edit setup.py to fix version detection
# Replace line 79 in setup.py:
#   OLD: version=get_version(),
#   NEW: version='1.4.2',

# Install
pip install -e .
cd ..
```

### Step 3: Install Real-ESRGAN

```bash
pip install realesrgan
```

### Step 4: Verify Installation

```bash
python -c "import basicsr; import realesrgan; print('Success!')"
```

## Simpler Alternative: Use Without Real-ESRGAN

The application includes a fallback optical flow-based upscaling that works without Real-ESRGAN:

1. Install core dependencies only (Step 1 above)
2. The app will automatically use fallback methods when Real-ESRGAN is not available
3. Performance will be lower but functional

## Test Your Installation

```bash
python test_app.py
```

This will check all dependencies and report any issues.
