from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "大宝贝！"

def yys_yuanjieshenpeng(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else default_text
    text2image = Text2Image.from_text(
        text, 60, fill=(255, 0, 0), stroke_width=2, stroke_fill="white",
        font_families=["GlowSansSC-Normal-Heavy"]
    ).wrap(500)
    if text2image.height > 200:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((160, 160), keep_ratio=True, inside=True)
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2 
        frame.paste(text_img, (x, 11), alpha=True)       
        return frame.copy().paste(img, (158, 119), alpha=True)

    return make_png_or_gif(images, make)


add_meme(
    "yys_yuanjieshenpeng",
    yys_yuanjieshenpeng,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["缘结神举", "缘结神捧"],
    date_created=datetime(2025, 10, 13),
    date_modified=datetime(2025, 10, 13),
)
