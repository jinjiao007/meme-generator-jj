from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "你闭嘴！"


def nizaishuo(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = f"{texts[0]}"
    text2image = Text2Image.from_text(
        text, 20, fill=(255, 255, 255), stroke_width=1, stroke_fill="black",
        font_families=["033-SSFangTangTi"]
    ).wrap(200)
    if text2image.height > 80:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((60, 50), keep_ratio=True, inside=True)
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(text_img, (x, 12), alpha=True)        
        return frame.copy().paste(img, (88, 14), alpha=True)

    return make_png_or_gif(images, make)


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
