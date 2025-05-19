from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def dafen(images: list[BuildImage], texts: list[str], args):
    try:
        if not images:
            raise ValueError("No images provided")
        img = images[0].convert("RGBA").resize((55, 55))  # 获取用户头像

        # 帧位置定义（从3到7帧的坐标）
        head_locs = [
            (46, 48), (46, 48), (31, 61), (31, 61), (34, 57)
        ]

        # 处理文本
        if not texts:
            raise ValueError("No text provided")
        text = f"{texts[0]}"
        text2image = Text2Image.from_text(
            text, 35, fill=(0, 0, 0), stroke_width=3, stroke_fill="white",
            font_families=["033-SSFangTangTi"]
        ).wrap(440)
        if text2image.height > 500:
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "0.png")  # 打开背景图
        for i in range(8):
            frame = BuildImage.new("RGBA", (background.width, background.height))
            # 粘贴 images 中的 0-7.png
            png_img = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png_img, alpha=True)
            # 从第3帧开始粘贴头像
            if i >= 3:
                if i - 3 < len(head_locs):
                    frame.paste(img, head_locs[i - 3], alpha=True)
                    # 粘贴文本 - 居中对齐
                    text_w, _ = text_img.size
                    x = (frame.width - text_w) // 2  # 居中对齐的x坐标
                    frame.paste(text_img, (165, 27), alpha=True)
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.08)  # 前7帧每帧0.08秒，最后一帧1秒

    except Exception as e:
        print(f"Error generating meme: {e}")
        return BytesIO()


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    if not frames:
        return BytesIO()
    buffer = BytesIO()

    # 为前7帧设置相同的时长，最后一帧设置为1秒（1000毫秒）
    durations = [int(duration * 1000)] * (len(frames) - 1) + [1000]

    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,  # 使用自定义时长列表
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer


add_meme(
    "dafen",
    dafen,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["满分"],
    keywords=["打分"],
    date_created=datetime(2025, 5, 17),
    date_modified=datetime(2025, 5, 17),
)