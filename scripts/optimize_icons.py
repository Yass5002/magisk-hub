#!/usr/bin/env python3
"""
Optimize and downscale raster icon images in assets/icons/
"""

import os
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def optimize_icons():
    icon_dir = os.path.join(REPO_ROOT, 'assets', 'icons')
    total_before = 0
    total_after = 0
    optimized_count = 0

    for f in sorted(os.listdir(icon_dir)):
        if not f.endswith(('.png', '.jpg', '.jpeg')):
            continue
        p = os.path.join(icon_dir, f)
        sz_before = os.path.getsize(p)
        total_before += sz_before

        try:
            with Image.open(p) as img:
                w, h = img.size
                if img.format != 'PNG' or img.mode != 'RGBA' or (w, h) != (512, 512):
                    img = img.convert('RGBA')
                    img = img.resize((512, 512), Image.Resampling.LANCZOS)
                    img.save(p, format='PNG', optimize=True)
                    sz_after = os.path.getsize(p)
                    optimized_count += 1
                    print(f"Normalized {f}: {w}x{h} ({sz_before/1024:.1f} KB) -> 512x512 ({sz_after/1024:.1f} KB)")
        except Exception as e:
            print(f"Skipping {f}: {e}")

        total_after += os.path.getsize(p)

    print(f"\nCompleted icon optimization:")
    print(f"Optimized {optimized_count} icons")
    print(f"Total directory size: {total_before/1024/1024:.2f} MB -> {total_after/1024/1024:.2f} MB")
    print(f"Reduction: {(1 - total_after/total_before)*100:.1f}%")

if __name__ == '__main__':
    optimize_icons()
