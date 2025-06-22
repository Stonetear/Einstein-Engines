#!/usr/bin/env python3
import os
from PIL import Image

# Set your textures root directory here
TEXTURES_ROOT = os.path.join(os.path.dirname(__file__), 'Resources', 'Textures')
SCALE_FACTOR = 2  # 32xN -> 64xN, 32x96 -> 64x192, etc.

def should_skip_dir(dirname):
    # Skip .rsi folders (handled by the other script)
    return dirname.lower().endswith('.rsi')

def resize_png(img_path, scale_factor):
    img = Image.open(img_path)
    # Skip files with width or height > 1024
    if img.width > 1024 or img.height > 1024:
        print(f"Skipping (too large): {img_path} ({img.width}x{img.height})")
        return
    new_size = (img.width * scale_factor, img.height * scale_factor)
    img = img.resize(new_size, Image.NEAREST)
    img.save(img_path)
    print(f"Resized: {img_path} to {new_size}")

def walk_and_resize_pngs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .rsi folders
        if should_skip_dir(os.path.basename(dirpath)):
            continue
        for file in filenames:
            if file.lower().endswith('.png'):
                img_path = os.path.join(dirpath, file)
                try:
                    resize_png(img_path, SCALE_FACTOR)
                except Exception as e:
                    print(f"Warning: Could not process {img_path}: {e}")

def main():
    walk_and_resize_pngs(TEXTURES_ROOT)
    print("Done.")

if __name__ == '__main__':
    main()
