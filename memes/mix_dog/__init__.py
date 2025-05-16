from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def mix_dog(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((85, 85))  # 用户头像

    # fmt: off
    locs = [
        (21, 90), (32, 50), (32, 16), (44, 9), (31, 16), (21, 27), 
        (21, 88), (0, 80)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "mix_dog",
    mix_dog,
    min_images=1,
    max_images=1,
    keywords=["小狗"],
    date_created=datetime(2025, 5, 14),
    date_modified=datetime(2025, 5, 14),
)