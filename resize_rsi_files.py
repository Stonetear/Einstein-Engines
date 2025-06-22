#!/usr/bin/env python3
import os
import json
from PIL import Image

# Set your textures root directory here
TEXTURES_ROOT = os.path.join(os.path.dirname(__file__), 'Resources', 'Textures')
NEW_SIZE = 64

def resize_spritesheet(img_path, frame_width, frame_height, new_size):
    img = Image.open(img_path)
    frames_x = img.width // frame_width
    frames_y = img.height // frame_height
    new_img = Image.new('RGBA', (frames_x * new_size, frames_y * new_size))
    for y in range(frames_y):
        for x in range(frames_x):
            left = x * frame_width
            upper = y * frame_height
            right = left + frame_width
            lower = upper + frame_height
            # Only process if the frame is fully inside the image
            if right <= img.width and lower <= img.height:
                box = (left, upper, right, lower)
                frame = img.crop(box)
                frame = frame.resize((new_size, new_size), Image.NEAREST)
                new_img.paste(frame, (x * new_size, y * new_size))
    new_img.save(img_path)


def process_rsi_folder(rsi_path):
    meta_path = os.path.join(rsi_path, 'meta.json')
    if not os.path.exists(meta_path):
        return
    try:
        with open(meta_path, 'r', encoding='utf-8-sig') as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse {meta_path}: {e}")
        return
    old_size = meta.get('size', [32, 32])
    # Ensure old_size is a list of two ints
    if not (isinstance(old_size, list) and len(old_size) == 2 and all(isinstance(x, int) for x in old_size)):
        old_size = [32, 32]
    if old_size == [NEW_SIZE, NEW_SIZE]:
        return  # Already resized
    # Resize all PNGs in the folder
    for file in os.listdir(rsi_path):
        if file.lower().endswith('.png'):
            img_path = os.path.join(rsi_path, file)
            try:
                resize_spritesheet(img_path, old_size[0], old_size[1], NEW_SIZE)
            except Exception as e:
                print(f"Warning: Could not process {img_path}: {e}")
    # Update meta.json, preserving original format (dict or list)
    if isinstance(meta.get('size'), dict):
        meta['size'] = {"x": NEW_SIZE, "y": NEW_SIZE}
    else:
        meta['size'] = [NEW_SIZE, NEW_SIZE]
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4)
    print(f"Resized: {rsi_path}")

def walk_and_resize(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'meta.json' in filenames:
            process_rsi_folder(dirpath)

def main():
    walk_and_resize(TEXTURES_ROOT)
    print("Done.")

if __name__ == '__main__':
    main()
