from datetime import datetime
from pathlib import Path
from math import pi, cos, sin
import numpy as np

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def yo_yo(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((55, 55))  # 用户头像

    # fmt: off
    locs = [
        (144, 58), (160, 57), (174, 55), (178, 42), (163, 31), (163, 27), 
        (150, 24), (150, 24), (50, 25), (39, 27), (28, 28), (28, 28),
        (28, 48), (39, 52), (51, 56)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(14):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "yo_yo",
    yo_yo,
    min_images=1,
    max_images=1,
    keywords=["yoyo"],
    date_created=datetime(2025, 5, 15),
    date_modified=datetime(2025, 5, 15),
)