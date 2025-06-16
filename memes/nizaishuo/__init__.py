from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "02大撒杯，闭嘴！"


def nizaishuo(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else default_text
    try:
        frame.draw_text(
            (12, 7, 86, 41),
            text,
            min_fontsize=10,
            max_fontsize=15,
            fill="white",
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((60, 50), keep_ratio=True, inside=True)
        return frame.copy().paste(img, (88, 14), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "nizaishuo",
    nizaishuo,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["你再说", "你闭嘴"],
    date_created=datetime(2025, 6, 16),
    date_modified=datetime(2025, 6, 16),
)
