from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def shadow_boxing(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((60, 60))  # 用户头像

    # fmt: off
    locs = [
        (133, 90), (133, 90), (133, 90), (120, 90), (108, 90), (108, 90)        
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(6):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.15)


add_meme(
    "shadow_boxing",
    shadow_boxing,
    min_images=1,
    max_images=1,
    keywords=["太极"],
    date_created=datetime(2025, 5, 14),
    date_modified=datetime(2025, 5, 14),
)