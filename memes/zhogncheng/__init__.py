from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "华为"

def zhongcheng(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else default_text
    text2image = Text2Image.from_text(
        text, 35, fill=(0, 0, 0), stroke_width=0, stroke_fill="red",
        font_families=["GlowSansSC-Normal-Heavy"]
    ).wrap(120)
    if text2image.height > 70:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    # 预处理用户头像（如果存在）
    user_head = None
    if len(images) > 1:  # 当有第二个图像（用户头像）时
        user_head = images[1].convert("RGBA").circle().resize((80, 80))

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((90, 90), keep_ratio=True, inside=True)
        frame_copy = frame.copy()
        frame_copy.paste(text_img, (202, 20), alpha=True)
        frame_copy.paste(img, (112, 74), alpha=True)
        
        # 仅当存在用户头像时粘贴
        if user_head:
            frame_copy.paste(user_head, (115, 172))
        
        return frame_copy

    return make_png_or_gif(images, make)


add_meme(
    "zhongcheng",
    zhongcheng,
    min_images=1,  
    max_images=2,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["忠诚"],
    date_created=datetime(2025, 6, 23),
    date_modified=datetime(2025, 6, 23),
)