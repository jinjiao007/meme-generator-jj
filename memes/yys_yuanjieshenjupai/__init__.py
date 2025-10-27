from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def yys_yuanjieshenjupai(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (60, 20, 249, 95),
            text,
            fill=(0, 0, 0),
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
    "yys_yuanjieshenjupai",
    yys_yuanjieshenjupai,
    min_texts=1,
    max_texts=1,
    default_texts=["阴阳师，启动！"],
    keywords=["缘结神举牌"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 10, 13),
    date_modified=datetime(2025, 10, 13),
)
