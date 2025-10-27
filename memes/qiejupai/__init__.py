from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"

default_text = "男銅！"

def qiejupai(images, texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (164, 10, 279, 108),
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
    "qiejupai",
    qiejupai,
    min_texts=1,
    max_texts=1,
    default_texts=[default_text],
    keywords=["企鹅举牌"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 10, 22),
    date_modified=datetime(2025, 10, 22),
)
