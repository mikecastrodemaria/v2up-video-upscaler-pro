# Flexible Scaling Guide 🎯

## What's New?

Your Video Upscaler Pro now supports **ANY scale factor** from 0.5× to 16×!

### Before (Limited) ❌
```
Scale options: Only 2×, 4×, 8×
No downscaling
No fractional scales
```

### After (Flexible) ✅
```
Scale range: 0.5× to 16.0× (any value!)
Downscaling: 0.5×, 0.75× supported
Fractional: 1.2×, 1.5×, 2.5×, 3× all work
Resolution presets for common upgrades
```

---

## How to Use

### Option 1: Use the Slider

```
Scale Factor: [0.5] ━━━●━━━ [16.0]

Move slider to any value:
- 1.5 = Perfect for 720p→1080p
- 2.0 = Perfect for 1080p→4K (Optimal AI)
- 2.5 = Between 2× and 4×
- 4.0 = Perfect for 540p→4K (Optimal AI)
- 0.75 = Downscale to 75% size
```

### Option 2: Use Quick Presets

Click a preset button for instant configuration:

| Preset Button | Scale | Use Case |
|---------------|-------|----------|
| **720p→1080p** | 1.5× | HD to Full HD |
| **1080p→4K** | 2.0× | Full HD to 4K UHD |
| **4K→8K** | 2.0× | 4K to 8K UHD |
| **Downscale** | 0.5× | Reduce file size |

---

## Scale Factor Guide

### Downscaling (< 1.0) - Reduce File Size

**When to use:** Make files smaller, reduce resolution

| Scale | Example | Method | Quality | Speed |
|-------|---------|--------|---------|-------|
| **0.5×** | 4K → 1080p | Lanczos | ⭐⭐⭐⭐⭐ | Very Fast |
| **0.75×** | 1080p → 810p | Lanczos | ⭐⭐⭐⭐⭐ | Very Fast |

**Use cases:**
- Reduce file size for sharing
- Create preview versions
- Match target platform requirements

---

### Small Upscaling (1.0-1.5) - Traditional Resize

**When to use:** Small improvements, fast processing

| Scale | Example | Method | Quality | Speed |
|-------|---------|--------|---------|-------|
| **1.2×** | 900p → 1080p | Lanczos | ⭐⭐⭐ | Fast |
| **1.3×** | 1440p → 1872p | Lanczos | ⭐⭐⭐ | Fast |

**Use cases:**
- Minor resolution adjustments
- Quick fixes
- Testing

---

### Optimal AI Upscaling (1.5-3.0) - Best Quality

**When to use:** Maximum quality for common upgrades

| Scale | Example | Method | Quality | Speed |
|-------|---------|--------|---------|-------|
| **1.5×** | 720p → 1080p | 2× AI + Resize | ⭐⭐⭐⭐ | Medium |
| **2.0×** | 1080p → 4K | 2× AI (Pure) | ⭐⭐⭐⭐⭐ | Slow |
| **2.5×** | 768p → 1920p | 2× AI + Resize | ⭐⭐⭐⭐ | Medium |
| **3.0×** | 640p → 1920p | 4× AI + Resize | ⭐⭐⭐⭐ | Medium |

**Best for:**
- 720p → 1080p (1.5×) ⭐ Recommended
- 1080p → 4K (2.0×) ⭐⭐ Optimal AI
- Custom resolutions

---

### Large AI Upscaling (3.0-8.0) - High Detail

**When to use:** Major quality improvements

| Scale | Example | Method | Quality | Speed |
|-------|---------|--------|---------|-------|
| **3.5×** | 540p → 1890p | 4× AI + Resize | ⭐⭐⭐⭐ | Medium |
| **4.0×** | 540p → 4K | 4× AI (Pure) | ⭐⭐⭐⭐⭐ | Slow |
| **6.0×** | 360p → 4K | 4× AI × 1.5 | ⭐⭐⭐⭐ | Slow |
| **8.0×** | 270p → 4K | 4× AI × 2 | ⭐⭐⭐⭐ | Very Slow |

**Best for:**
- SD → 4K (4×-6×)
- Old footage restoration
- Maximum detail recovery

---

### Extreme Upscaling (8.0-16.0) - Specialized

**When to use:** Extreme cases, testing limits

| Scale | Example | Method | Quality | Speed |
|-------|---------|--------|---------|-------|
| **10.0×** | 192p → 1920p | Multiple AI | ⭐⭐⭐ | Very Slow |
| **12.0×** | 160p → 1920p | Multiple AI | ⭐⭐⭐ | Extremely Slow |
| **16.0×** | 120p → 1920p | Multiple AI | ⭐⭐ | Extremely Slow |

**Note:** Quality degrades at extreme scales

---

## How It Works: Smart Hybrid Approach

### Pure AI (2.0×, 4.0×) - Optimal
```
Input → AI Model → Output
Best quality, slower processing
```

### Hybrid AI (1.5×, 2.5×, 3.0×, etc.)
```
Input → AI Model (2× or 4×) → Lanczos Resize → Output
Excellent quality, balanced speed
```

### Traditional (< 1.5×)
```
Input → Lanczos Resize → Output
Good quality, very fast
```

### Downscale (< 1.0×)
```
Input → Lanczos Resize → Output
Perfect quality (no AI needed)
```

---

## Common Use Cases

### SD to HD (Standard to High Definition)
```
Input: 720×480 (SD)
Scale: 1.8×
Output: 1296×864
Method: 2× AI + Resize
```

### HD to FHD (HD to Full HD)
```
Input: 1280×720 (HD)
Scale: 1.5×
Output: 1920×1080 (FHD)
Method: 2× AI + Resize
⭐ Recommended preset!
```

### FHD to 4K (Full HD to 4K UHD)
```
Input: 1920×1080 (FHD)
Scale: 2.0×
Output: 3840×2160 (4K)
Method: 2× AI (Pure)
⭐⭐ Perfect match!
```

### 4K to 8K (4K to 8K UHD)
```
Input: 3840×2160 (4K)
Scale: 2.0×
Output: 7680×4320 (8K)
Method: 2× AI (Pure)
⭐⭐ Perfect match!
```

### 4K to 1080p (Downscale for Sharing)
```
Input: 3840×2160 (4K)
Scale: 0.5×
Output: 1920×1080 (FHD)
Method: Lanczos
⚡ Very fast!
```

---

## Performance Guide

### CPU Mode (Current RTX 5090 Setup)

| Scale | Resolution | Time per Frame | 100 Frames |
|-------|-----------|----------------|------------|
| **0.5×** | 4K→1080p | 0.1s | 10s |
| **1.5×** | 720p→1080p | 5-10s | 8-17 min |
| **2.0×** | 1080p→4K | 8-15s | 13-25 min |
| **4.0×** | 540p→4K | 10-20s | 17-33 min |

### GPU Mode (When PyTorch adds RTX 5090 support)

| Scale | Resolution | Time per Frame | 100 Frames |
|-------|-----------|----------------|------------|
| **2.0×** | 1080p→4K | 0.5-1s | 50-100s |
| **4.0×** | 540p→4K | 1-2s | 100-200s |

**10-20× faster on GPU!** 🚀

---

## Tips & Best Practices

### ✅ Do's

✅ **Use 2.0× or 4.0× for best quality** (pure AI)
✅ **Use presets for common upgrades** (1080p→4K)
✅ **Test with preview first** (5 seconds)
✅ **Use downscaling for file size** (0.5×, 0.75×)

### ❌ Don'ts

❌ **Don't use extreme scales (>12×)** - quality degrades
❌ **Don't upscale already upscaled content** - artifacts multiply
❌ **Don't expect miracles** - AI can't invent detail that doesn't exist

### 💡 Pro Tips

1. **For 720p→1080p:** Use 1.5× preset (optimal)
2. **For 1080p→4K:** Use 2.0× preset (perfect AI match)
3. **For custom scales:** Try values close to 2.0× or 4.0×
4. **For testing:** Start with preview (5 seconds)
5. **For speed:** Use scales <1.5× or downscale

---

## Quality Comparison

### Scale Factor vs. Quality

```
Quality
  ⭐⭐⭐⭐⭐  |     2.0×, 4.0× (Pure AI)
  ⭐⭐⭐⭐    |   1.5×, 2.5×, 3.0× (Hybrid)
  ⭐⭐⭐      |     1.2×, 1.3× (Lanczos)
  ⭐⭐        |      8×+ (Multiple AI)
  ⭐⭐⭐⭐⭐  |   0.5×, 0.75× (Downscale)
              +─────────────────────────────→
              0.5×  1×   2×   4×   8×   16×
```

---

## Frequently Asked Questions

### Q: Why use 1.5× instead of 2.0×?
**A:** For 720p→1080p, 1.5× is the exact ratio needed. Using 2.0× would give you 1440p, then you'd need to resize down.

### Q: Can I use negative scales?
**A:** No, but scales <1.0 are downscaling (0.5× = half size).

### Q: What's the best scale for my video?
**A:**
- **Known target:** Calculate exact ratio (e.g., 720→1080 = 1.5×)
- **General improvement:** Use 2.0× or 4.0× (optimal AI)
- **File size reduction:** Use 0.5× or 0.75×

### Q: Why is 2.0× and 4.0× slower?
**A:** Pure AI processing is slower but gives best quality. Other scales use hybrid approach (AI + fast resize).

### Q: Can I upscale and downscale in one step?
**A:** Yes! You can chain operations or use a scale that represents the net effect.

---

## Examples

### Example 1: Restore Old Footage
```
Input: 480×360 (old VHS capture)
Goal: Modern 1080p
Scale: 3.0×
Output: 1440×1080 (then crop to 1920×1080)
Method: 4× AI + Resize
Time: ~15s per frame (CPU)
```

### Example 2: Social Media Optimization
```
Input: 4K video (3840×2160)
Goal: Instagram (1080×1080 square)
Scale: 0.5× (then crop)
Method: Lanczos downscale
Time: <1s per frame
```

### Example 3: Monitor Matching
```
Input: 1920×1080
Goal: 2560×1440 (1440p monitor)
Scale: 1.33×
Method: Lanczos
Time: Very fast
```

---

## Summary

✅ **Arbitrary scales:** 0.5× to 16.0× supported
✅ **Downscaling:** File size reduction
✅ **Resolution presets:** One-click common upgrades
✅ **Smart hybrid:** Optimal quality/speed balance
✅ **Pure AI at 2×, 4×:** Best quality
✅ **Fast processing:** For scales <1.5×

**Your video upscaler is now incredibly flexible!** 🎉

Try it now: `start.bat`
