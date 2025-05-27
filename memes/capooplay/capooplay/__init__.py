from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def capooplay(images: list[BuildImage], texts, args):
    try:
        if not images:
            raise ValueError("No images provided")
        img = images[0].convert("RGBA").resize((80, 80))  # 获取用户头像

        # 帧位置定义
        head_locs = [
            (20, 201), (18, 201), (20, 201), (18, 201), (20, 201), (18, 201), 
            (20, 201), (18, 201), (20, 201), (18, 201), (20, 201), (18, 201), 
            (20, 201), (18, 201), (20, 201), (18, 201), (20, 201), (18, 201), 
        ]

        # 获取 0.png 的图像大小
        background_img = BuildImage.open(img_dir / "0.png")
        width, height = background_img.width, background_img.height

        # 创建动态帧
        frames = []
        for i in range(18):
            # 生成透明背景图
            frame = BuildImage.new("RGBA", (width, height))
            # 粘贴用户头像到指定坐标位置
            frame.paste(img, head_locs[i], alpha=True)
            # 粘贴 0-21.png
            png_img = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png_img, alpha=True)
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.05)

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
    "capooplay",
    capooplay,
    min_images=1,
    max_images=1,
    keywords=["咖波打"],
    date_created=datetime(2025, 5, 27),
    date_modified=datetime(2025, 5, 27),
)