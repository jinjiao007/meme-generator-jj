from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def kurogames_chun_holdsign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (53, 286, 312, 458),
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
    "kurogames_chun_holdsign",
    kurogames_chun_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["傻？我不傻"],
    keywords=["椿举牌", "大傻椿举牌"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 6, 30),
    date_modified=datetime(2025, 6, 30),
)
