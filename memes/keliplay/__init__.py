from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def keliplay(images: list[BuildImage], texts, args):
    try:
        if not images:
            raise ValueError("No images provided")
        img = images[0].convert("RGBA").resize((109, 109))  # 获取用户头像

        # 帧位置定义
        head_locs = [
            (71, 38), (71, 38), (95, 38), (113, 45), (90, 41), (66, 41), 
            (91, 41), (111, 46), (87, 74), (74, 89), (61, 101), (63, 76),
            (66, 57), (68, 52), (67, 43), (67, 46), (79, 55), (66, 44), 
            (79, 52), (90, 52), (116, 57), (131, 57), (71, 59), (78, 62),
            (93, 85), (93, 85), (99, 95), (106, 107), (130, 31), (130, 31), 
            (130, 31), (130, 31)
        ]

        # 获取 0.png 的图像大小
        background_img = BuildImage.open(img_dir / "0.png")
        width, height = background_img.width, background_img.height

        # 创建动态帧
        frames = []
        for i in range(32):
            # 生成透明背景图
            frame = BuildImage.new("RGBA", (width, height))
            # 粘贴用户头像到指定坐标位置
            if i < len(head_locs):
                frame.paste(img, head_locs[i], alpha=True)
            # 粘贴 0-31.png
            png_img = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png_img, alpha=True)
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.08)

    except Exception as e:
        print(f"Error generating meme: {e}")
        return BytesIO()


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    if not frames:
        return BytesIO()

    buffer = BytesIO()
    # 为所有帧设置相同的时长
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=int(duration * 1000),
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer


add_meme(
    "keliplay",
    keliplay,
    min_images=1,
    max_images=1,
    keywords=["可莉打"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)