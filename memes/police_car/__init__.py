from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def police_car(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((36, 36))
    # fmt: off
    locs = [
        (81, 53), (81, 51), (81, 49), (81, 51), (81, 53), (81, 51),
        (81, 49), (81, 51), (81, 53), (81, 51), (81, 49), (81, 51), 
        (81, 53), (81, 51), (81, 49), (81, 51), (81, 53), (81, 51),
        (81, 49), (81, 51), (81, 53), (81, 51), (81, 49), (81, 51),
        (81, 53), (81, 51), (81, 49), (81, 51), (81, 53), (81, 51),
        (81, 49), (81, 51), (81, 53), (81, 51), (81, 49), (81, 51),
        (81, 53), (81, 51), (81, 49), (81, 51), (81, 53), (81, 51),
        (81, 49), (81, 51), (81, 53), (81, 51)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(45):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "police_car",
    police_car,
    min_images=1,
    max_images=1,
    keywords=["警车"],
    date_created=datetime(2025, 5, 13),
    date_modified=datetime(2025, 5, 13),
)