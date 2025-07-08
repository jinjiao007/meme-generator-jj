from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def gulaojupai(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (28, 280, 450, 455),
            text,
            fill=(255, 255, 255),
            allow_wrap=True,
            max_fontsize=60,
            min_fontsize=20,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "gulaojupai",
    gulaojupai,
    min_texts=1,
    max_texts=1,
    default_texts=["我叫小萌新"],
    keywords=["故佬举牌", "小萌新举牌"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 7, 8),
    date_modified=datetime(2025, 7, 8),
)
