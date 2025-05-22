from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "我是芙蓉王，请v我50"


def fulilianv50(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "v50.png")
    try:
        frame.draw_text(
            (9, 14, frame.width - 9, 60),
            text,
            max_fontsize=25,
            min_fontsize=18,
            fill="black",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((120, 120), keep_ratio=True)
        return frame.copy().paste(img, (120, 89), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "fulilianv50",
    fulilianv50,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["芙莉莲v50"],
    date_created=datetime(2025, 5, 22),
    date_modified=datetime(2025, 5, 22),
)
