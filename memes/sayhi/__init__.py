from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def sayhi(images: list[BuildImage], texts: list[str], args):

    img = images[0].convert("RGBA").resize((80, 80))  # 获取用户头像
    # 帧位置定义
    locs = [
        (27, 95), (28, 95), (22, 102), (17, 100), (16, 101), (17, 101),
        (20, 108), (43, 115), (42, 99), (42, 99), (42, 99), (42, 99),
        (42, 99), (42, 99), (42, 99), (40, 99)
        ]

    # 处理文本
    text = f"打个招呼吧，{texts[0]}"
    text2image = Text2Image.from_text(
        text, 25, fill=(0, 0, 0), stroke_width=3, stroke_fill="white",
        font_families=["033-SSFangTangTi"]
        ).wrap(320)
    if text2image.height > 100:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    # 创建动态帧
    frames: list[IMG] = []
    background = BuildImage.open(img_dir / "0.png")  # 打开背景图
    for i in range(16):
        frame = BuildImage.new("RGBA", (background.width, background.height))
        png_img = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frame.paste(png_img, alpha=True)        
        # 粘贴文本 - 居中对齐
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(text_img, (x, 306), alpha=True)
        frames.append(frame.image)

    # 返回 GIF 动画
    return save_gif(frames, 0.08) 



add_meme(
    "sayhi",
    sayhi,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["小奶龙"],
    keywords=["打招呼"],
    date_created=datetime(2025, 6, 25),
    date_modified=datetime(2025, 6, 25),
)