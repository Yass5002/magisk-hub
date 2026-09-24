#!/usr/bin/env python3
"""
Optimize and downscale raster icon images in assets/icons/
"""

import os
from PIL import Image

def optimize_icons():
    icon_dir = 'assets/icons'
    total_before = 0
    total_after = 0
    optimized_count = 0

    for f in sorted(os.listdir(icon_dir)):
        if not f.endswith(('.png', '.jpg', '.jpeg')):
            continue
        p = os.path.join(icon_dir, f)
        sz_before = os.path.getsize(p)
        total_before += sz_before

        # Check if it is a valid raster image
        try:
            with Image.open(p) as img:
                w, h = img.size
                if w > 128 or h > 128 or sz_before > 20000:
                    img = img.convert('RGBA')
                    img.thumbnail((128, 128), Image.Resampling.LANCZOS)
                    img.save(p, format='PNG', optimize=True)
                    sz_after = os.path.getsize(p)
                    optimized_count += 1
                    print(f"Optimized {f}: {w}x{h} ({sz_before/1024:.1f} KB) -> {img.size[0]}x{img.size[1]} ({sz_after/1024:.1f} KB)")
        except Exception as e:
            # SVG or non-PIL format - leave as is
            pass

        total_after += os.path.getsize(p)

    print(f"\nCompleted icon optimization:")
    print(f"Optimized {optimized_count} icons")
    print(f"Total directory size: {total_before/1024/1024:.2f} MB -> {total_after/1024/1024:.2f} MB")
    print(f"Reduction: {(1 - total_after/total_before)*100:.1f}%")

if __name__ == '__main__':
    optimize_icons()
