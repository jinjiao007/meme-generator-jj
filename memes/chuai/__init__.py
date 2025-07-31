from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def chuai(images: list[BuildImage], texts, args):

    img = images[0].convert("RGBA").circle().resize((80, 80))  # 获取用户头像
    # 帧位置定义
    locs = [
        (14, 220), (14, 220), (14, 220), (14, 220),  # 0-3帧
        (14, 220), (14, 220), (14, 220), (14, 220),  # 4-7帧
        (14, 220), (14, 220), (14, 220), (14, 220),  # 8-11帧
        (14, 220), (14, 220), (14, 220), (14, 220),  # 12-15帧
        (12, 220), (10, 220), (5, 220), (10, 220),  # 16-19帧
        (14, 220), (14, 220)                        # 20-21帧
    ]


    # 创建动态帧
    frames: list[IMG] = []
    background = BuildImage.open(img_dir / "0.png")  # 打开背景图
    for i in range(22):
        frame = BuildImage.new("RGBA", (background.width, background.height))
        png_img = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(png_img, alpha=True)
        frame.paste(img, locs[i], alpha=True)        
        frames.append(frame.image)

    # 返回 GIF 动画
    return save_gif(frames, 0.04) 



add_meme(
    "chuai",
    chuai,
    min_images=1,
    max_images=1,
    keywords=["踹"],
    date_created=datetime(2025, 7, 31),
    date_modified=datetime(2025, 7, 31),
)