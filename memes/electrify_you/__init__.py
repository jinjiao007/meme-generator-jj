from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def electrify_you(images: list[BuildImage], texts: list[str], args):
    try:
        if not images:
            raise ValueError("No images provided")
        
        # 获取用户头像并转换为圆形
        img = images[0].convert("RGBA").circle().resize((118, 85))

        # 帧位置定义
        locs= [(68, 82), (62, 80)]  

        # 处理文本
        if not texts:
            raise ValueError("No text provided")
        text = f"电死你个 {texts[0]}"
        text2image = Text2Image.from_text(
            text, 25, fill=(0, 0, 0), stroke_width=1, stroke_fill="yellow",
            font_families=["033-SSFangTangTi"]
        ).wrap(440)
        if text2image.height > 500:
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "0.png")  # 打开背景图
        for i in range(2):
            frame = BuildImage.new("RGBA", (background.width, background.height))           
            frame.paste(img, locs[i], alpha=True)
            png_img = BuildImage.open(img_dir / f"{i}.png")    
            frame.paste(png_img, alpha=True)       
            # 粘贴文本 - 居中对齐
            text_w, _ = text_img.size
            x = (frame.width - text_w) // 2  # 居中对齐的x坐标
            frame.paste(text_img, (x, 12), alpha=True)
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.08)  # 前6帧每帧0.08秒，最后一帧1秒

    except Exception as e:
        print(f"Error generating meme: {e}")
        return BytesIO()


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    if not frames:
        return BytesIO()


    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer


add_meme(
    "electrify_you",
    electrify_you,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["猪头"],
    keywords=["电死你"],
    date_created=datetime(2025, 5, 20),
    date_modified=datetime(2025, 5, 20),
)