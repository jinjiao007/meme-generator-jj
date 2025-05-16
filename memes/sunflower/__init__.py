from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def sunflower(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((90, 90))  # 用户头像

    # fmt: off
    locs = [
        (91, 121), (91, 107), (91, 85), (91, 98), (91, 85), (100, 93), 
        (100, 108), (100, 114), (105, 128), (109, 130)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(10):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "sunflower",
    sunflower,
    min_images=1,
    max_images=1,
    keywords=["太阳花"],
    date_created=datetime(2025, 5, 14),
    date_modified=datetime(2025, 5, 14),
)