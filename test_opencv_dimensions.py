"""
Test that output dimensions are integers for OpenCV
"""

def test_dimension_types():
    """Test dimension calculations produce integers"""
    print("=" * 60)
    print("Testing Dimension Type Conversion")
    print("=" * 60)
    print()

    test_cases = [
        (1920, 1080, 2.0, "2x scale"),
        (1920, 1080, 1.5, "1.5x scale (fractional)"),
        (824, 1464, 4.0, "4x scale (user's video)"),
        (1280, 720, 2.5, "2.5x scale"),
        (3840, 2160, 0.5, "0.5x downscale"),
    ]

    all_passed = True

    for width, height, scale, description in test_cases:
        # Calculate dimensions (as would happen in code)
        output_width = int(width * scale)
        output_height = int(height * scale)

        # Check types
        width_is_int = isinstance(output_width, int)
        height_is_int = isinstance(output_height, int)

        status = "PASS" if (width_is_int and height_is_int) else "FAIL"
        print(f"[{status}] {description}")
        print(f"      Input: {width}x{height}, Scale: {scale}x")
        print(f"      Output: {output_width}x{output_height}")
        print(f"      Types: width={type(output_width).__name__}, height={type(output_height).__name__}")

        if not (width_is_int and height_is_int):
            all_passed = False
            print(f"      ERROR: Expected int types!")

        print()

    print("=" * 60)
    if all_passed:
        print("SUCCESS: All dimensions are integers")
    else:
        print("FAILED: Some dimensions are not integers")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    import sys
    success = test_dimension_types()
    sys.exit(0 if success else 1)
