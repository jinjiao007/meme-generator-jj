from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def andwho(images: list[BuildImage], texts: list[str], args):
    text = f"{texts[0]}"

    # 动态字号：72 ～ 24
    max_size = 72
    min_size = 24
    size = max_size

    while size >= min_size:
        text2image = Text2Image.from_text(
            text,
            size,
            fill=(0, 0, 0),
            stroke_width=1,
            stroke_fill="black",
            font_families=["GlowSansSC-Normal-Heavy"],
        ).wrap(253)

        if text2image.height <= 170:
            break
        size -= 2  # 每次降 2 号，也可以改成 1 号更细腻
    else:
        # 字号已经降到 24 仍然溢出
        raise TextOverLength(text)

    text_img = text2image.to_image()

    background = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").square().resize((300, 300))
        frame = BuildImage.new("RGBA", background.size, (0, 0, 0, 0))
        frame.paste(img, (430, 272), alpha=True)
        frame.paste(background, (0, 0), alpha=True)

        # 计算居中坐标
        x = 0 + (252 - text_img.width) // 2  # 水平居中
        y = 444 + (171 - text_img.height) // 2  # 垂直居中
        frame.paste(text_img, (x, y), alpha=True)
        return frame

    return make_png_or_gif(images, make)


add_meme(
    "andwho",
    andwho,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["原神"],
    keywords=["今天和谁过"],
    date_created=datetime(2025, 8, 29),
    date_modified=datetime(2025, 8, 29),
)