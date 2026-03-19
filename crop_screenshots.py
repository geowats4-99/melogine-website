#!/usr/bin/env python3
"""Crop status bars from Melogine screenshots. Saves to screenshots/ subfolder."""

import os
import shutil
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
STATUS_BAR_HEIGHT = 130
RADAR_IMAGE = "IMG_4755.PNG"

# All screenshots to process. New screenshot saved as IMG_challenges_correct.PNG first.
SOURCE_FILES = [
    "IMG_4725.PNG",
    "IMG_4726.PNG",
    "IMG_4727.PNG",
    "IMG_4728.PNG",
    "IMG_4730.PNG",
    "IMG_4731.PNG",
    "IMG_4732.PNG",
    "IMG_4742.PNG",
    "IMG_4744.PNG",
    "IMG_4755.PNG",
    "IMG_4756.PNG",
]

# Newly attached screenshot - copy from this name first
NEW_SCREENSHOT_SOURCE = "Screenshot 2026-03-19 at 17.26.10.png"
NEW_SCREENSHOT_DEST = "IMG_challenges_correct.PNG"


def main():
    out_dir = SCRIPT_DIR / "screenshots"
    out_dir.mkdir(exist_ok=True)

    # Copy new screenshot to IMG_challenges_correct.PNG if it exists
    new_src = SCRIPT_DIR / NEW_SCREENSHOT_SOURCE
    if new_src.exists():
        shutil.copy2(new_src, SCRIPT_DIR / NEW_SCREENSHOT_DEST)
        print(f"Copied {NEW_SCREENSHOT_SOURCE} -> {NEW_SCREENSHOT_DEST}")

    all_files = SOURCE_FILES + [NEW_SCREENSHOT_DEST]

    for filename in all_files:
        src = SCRIPT_DIR / filename
        if not src.exists():
            print(f"Skip (not found): {filename}")
            continue

        img = Image.open(src).convert("RGBA")
        w, h = img.size

        if filename == RADAR_IMAGE:
            # Crop to square: center, based on shorter dimension
            size = min(w, h)
            left = (w - size) // 2
            top = (h - size) // 2
            cropped = img.crop((left, top, left + size, top + size))
        else:
            # Remove top 130px (status bar)
            cropped = img.crop((0, STATUS_BAR_HEIGHT, w, h))

        out_path = out_dir / filename
        cropped.save(out_path, "PNG")
        print(f"Cropped: {filename} -> screenshots/{filename}")


if __name__ == "__main__":
    main()
