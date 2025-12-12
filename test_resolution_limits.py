"""
Test resolution limit checks for various video orientations
"""

def test_resolution_limit(width, height, description):
    """Test if resolution passes the limit check"""
    output_megapixels = (width * height) / (1024 * 1024)
    max_megapixels = 33.2  # 8K = 7680x4320 = 33.2 MP

    passes = output_megapixels <= max_megapixels
    status = "PASS" if passes else "FAIL"
    percentage = (output_megapixels / max_megapixels) * 100

    print(f"[{status}] {description}")
    print(f"      Resolution: {width}x{height}")
    print(f"      Megapixels: {output_megapixels:.2f} MP ({percentage:.1f}% of limit)")
    print()

    return passes

print("=" * 60)
print("Testing Resolution Limits")
print("=" * 60)
print()

# Test cases
results = []

# User's actual video (portrait, 4x upscale from 824x1464)
results.append(test_resolution_limit(
    3296, 5856,
    "User's video (portrait 824x1464 to 3296x5856)"
))

# Standard 8K landscape
results.append(test_resolution_limit(
    7680, 4320,
    "8K Landscape (exactly at limit)"
))

# Standard 4K landscape upscaled 2x
results.append(test_resolution_limit(
    3840 * 2, 2160 * 2,
    "4K Landscape 2x upscale (7680x4320)"
))

# 1080p portrait upscaled 4x
results.append(test_resolution_limit(
    1080 * 4, 1920 * 4,
    "1080p Portrait 4x upscale (4320x7680)"
))

# Extreme portrait (should fail)
results.append(test_resolution_limit(
    2160 * 4, 3840 * 4,
    "4K Portrait 4x upscale (8640x15360) - SHOULD FAIL"
))

# Summary
print("=" * 60)
print("Summary")
print("=" * 60)
passed = sum(results)
total = len(results)
print(f"Passed: {passed}/{total}")
print()

if results[0]:
    print("SUCCESS: User's video will now work!")
else:
    print("ERROR: User's video still blocked")
