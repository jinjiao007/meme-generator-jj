from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "给你V50"


def vni50(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (29, 184, 222, 239),
            text,
            max_fontsize=25,
            min_fontsize=18,
            fill="#fce4b8",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((60, 60), keep_ratio=True)
        return frame.copy().paste(img, (97, 62), below=True)

    return make_png_or_gif(images, make)


add_meme(
    "vni50",
    vni50,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["v你50"],
    date_created=datetime(2025, 8, 7),
    date_modified=datetime(2025, 8, 7),
)
