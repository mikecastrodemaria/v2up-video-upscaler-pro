"""
Fix for basicsr compatibility with newer torchvision versions.
This script patches the degradations.py file in basicsr to work with torchvision 0.20+
where functional_tensor was merged into functional.
"""
import os
import sys

def fix_basicsr_imports():
    """Fix the torchvision import in basicsr degradations.py"""

    # Find the basicsr installation
    # Try importing first, but if it fails due to the import error, find it manually
    try:
        import basicsr
        basicsr_path = os.path.dirname(basicsr.__file__)
    except Exception as e:
        # If import fails, try to find it in site-packages
        import site
        site_packages = site.getsitepackages()
        basicsr_path = None
        for sp in site_packages:
            potential_path = os.path.join(sp, 'basicsr')
            if os.path.exists(potential_path):
                basicsr_path = potential_path
                break

        if basicsr_path is None:
            print(f"ERROR: basicsr is not installed or could not be found")
            print(f"Import error: {e}")
            return False
        else:
            print(f"Found basicsr at: {basicsr_path} (couldn't import due to error)")

    degradations_file = os.path.join(basicsr_path, 'data', 'degradations.py')

    if not os.path.exists(degradations_file):
        print(f"ERROR: Could not find {degradations_file}")
        return False

    print(f"Patching: {degradations_file}")

    # Read the file
    with open(degradations_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already patched
    if 'PATCHED FOR TORCHVISION 0.20+' in content:
        print("File is already patched!")
        return True

    # Replace the problematic import
    old_import = "from torchvision.transforms.functional_tensor import rgb_to_grayscale"
    new_import = """# PATCHED FOR TORCHVISION 0.20+: functional_tensor merged into functional
try:
    from torchvision.transforms.functional_tensor import rgb_to_grayscale
except (ImportError, ModuleNotFoundError):
    from torchvision.transforms.functional import rgb_to_grayscale"""

    if old_import in content:
        content = content.replace(old_import, new_import)

        # Write back the file
        with open(degradations_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("Successfully patched basicsr!")
        print("The import error should now be fixed.")
        return True
    else:
        print("WARNING: Could not find the expected import statement.")
        print("The file may have already been modified or is a different version.")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("basicsr Torchvision Compatibility Fix")
    print("=" * 60)
    print()

    success = fix_basicsr_imports()

    print()
    if success:
        print("Testing import...")
        try:
            import realesrgan
            print("SUCCESS: realesrgan can now be imported!")
        except Exception as e:
            print(f"WARNING: realesrgan still has issues: {e}")
    else:
        print("FAILED: Could not patch basicsr")
        sys.exit(1)
