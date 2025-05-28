from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def zhuishamiao(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((60, 48))  # 将用户头像转换为圆形
    
    # 0-10帧中头像的位置和大小
    locs = [
        (23, 59), (24, 60), (29, 57), (32, 60), (34, 58), (43, 60), 
        (46, 60), (43, 58), (43, 60), (43, 63), (41, 62), (39, 64), 
        (45, 61), (46, 55), (43, 57), (41, 56), (40, 52), (37, 52), 
        (33, 49), (33, 53), (37, 50), (39, 49), (41, 49), (44, 50), 
        (44, 52)
    ]

    frames: list[IMG] = []
    for i in range(25):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 获取 locs 的位置和大小
        frame.paste(img, locs[i], alpha=True)      
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "zhuishamiao",
    zhuishamiao,
    min_images=1,
    max_images=1,
    keywords=["追杀喵"],
    date_created=datetime(2025, 5, 28),
    date_modified=datetime(2025, 5, 28),
)