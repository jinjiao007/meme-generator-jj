from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def houminghao(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (31, 19, 508, 274),
            text,
            fill=(81, 96, 115),
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
    "houminghao",
    houminghao,
    min_texts=1,
    max_texts=1,
    default_texts=["姐姐不乖哦"],
    keywords=["侯明昊"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 7, 11),
    date_modified=datetime(2025, 7, 11),
)
