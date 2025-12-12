"""
Environment Test Script for v2up Video Upscaler Pro
Tests all critical components to ensure proper setup
"""

import sys
import struct

def test_python_version():
    """Test Python version and architecture"""
    print("=" * 60)
    print("Testing Python Environment")
    print("=" * 60)

    version = sys.version
    arch = struct.calcsize('P') * 8

    print(f"Python version: {version}")
    print(f"Architecture: {arch}-bit")

    # Check if beta by looking at the version tuple
    version_tuple = sys.version_info
    version_str = f"{version_tuple.major}.{version_tuple.minor}.{version_tuple.micro}"

    # Check for beta/RC/alpha in the release level
    is_beta = version_tuple.releaselevel in ['alpha', 'beta', 'candidate']

    if is_beta:
        print(f"WARNING: Beta/RC/Alpha Python detected! ({version_tuple.releaselevel})")
        return False
    else:
        print(f"Status: STABLE RELEASE ({version_str})")
        return True

def test_orjson():
    """Test orjson import and basic functionality"""
    print("\n" + "=" * 60)
    print("Testing orjson")
    print("=" * 60)

    try:
        import orjson
        print(f"orjson version: {orjson.__version__}")

        # Test basic serialization
        test_data = {"test": "data", "number": 42}
        serialized = orjson.dumps(test_data)
        deserialized = orjson.loads(serialized)

        if deserialized == test_data:
            print("Status: WORKING")
            return True
        else:
            print("ERROR: Serialization test failed")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_pytorch():
    """Test PyTorch and CUDA"""
    print("\n" + "=" * 60)
    print("Testing PyTorch and CUDA")
    print("=" * 60)

    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")

        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"cuDNN version: {torch.backends.cudnn.version()}")
            print(f"GPU count: {torch.cuda.device_count()}")

            if torch.cuda.device_count() > 0:
                device_name = torch.cuda.get_device_name(0)
                print(f"GPU 0: {device_name}")

                # Test tensor creation on GPU
                test_tensor = torch.randn(3, 3).cuda()
                print(f"Tensor device: {test_tensor.device}")
                print("Status: CUDA WORKING")
        else:
            print("WARNING: CUDA not available (CPU-only mode)")

        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_core_packages():
    """Test core ML/Vision packages"""
    print("\n" + "=" * 60)
    print("Testing Core Packages")
    print("=" * 60)

    packages = {
        'gradio': 'Gradio',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'PIL': 'Pillow',
        'tqdm': 'tqdm',
    }

    results = []
    for module_name, display_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"[OK] {display_name}: {version}")
            results.append(True)
        except Exception as e:
            print(f"[FAIL] {display_name}: {e}")
            results.append(False)

    return all(results)

def test_ai_packages():
    """Test AI model packages"""
    print("\n" + "=" * 60)
    print("Testing AI Model Packages")
    print("=" * 60)

    packages = [
        ('basicsr', 'BasicSR'),
        ('realesrgan', 'Real-ESRGAN'),
    ]

    results = []
    for module_name, display_name in packages:
        try:
            module = __import__(module_name)
            print(f"[OK] {display_name}")
            results.append(True)
        except Exception as e:
            print(f"[FAIL] {display_name}: {e}")
            results.append(False)

    return all(results)

def main():
    """Run all tests"""
    print("\n")
    print("*" * 60)
    print("v2up Video Upscaler Pro - Environment Test")
    print("*" * 60)
    print("\n")

    results = {
        'Python Environment': test_python_version(),
        'orjson': test_orjson(),
        'PyTorch/CUDA': test_pytorch(),
        'Core Packages': test_core_packages(),
        'AI Packages': test_ai_packages(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        symbol = "[OK]" if passed else "[XX]"
        print(f"{symbol} {test_name}: {status}")

    print("\n" + "=" * 60)

    if all(results.values()):
        print("SUCCESS: All tests passed!")
        print("Your environment is ready to use.")
        return 0
    else:
        print("WARNING: Some tests failed.")
        print("Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\n")
    sys.exit(exit_code)
