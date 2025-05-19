from datetime import datetime
from pathlib import Path
from math import pi, cos, sin
import numpy as np

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def doroya(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((192, 156))  # 用户头像

    # fmt: off
    locs = [
        (88, 82), (88, 85), (52, 89), (90, 77), (84, 88), (52, 88)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(6):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "doroya",
    doroya,
    min_images=1,
    max_images=1,
    keywords=["doro鸭"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)