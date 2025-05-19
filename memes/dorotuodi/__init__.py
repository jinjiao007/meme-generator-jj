from datetime import datetime
from pathlib import Path
from math import pi, cos, sin
import numpy as np

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def dorotuodi(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((61, 55))  # 用户头像

    # fmt: off
    locs = [
        (81, 64), (81, 60), (78, 64), (78, 59), (78, 58)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(5):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "dorotuodi",
    dorotuodi,
    min_images=1,
    max_images=1,
    keywords=["doro拖地"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)