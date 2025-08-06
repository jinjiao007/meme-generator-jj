from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def doroqi(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((80, 80)) # 将用户头像转换为圆形
    
    # 0-18帧中头像的位置和大小
    locs = [
        (125, 121), (114, 135), (113, 130), (109, 138), (108, 134),
        (105, 140), (105, 137), (103, 141), (100, 144), (108, 129),
        (117, 121), (111, 126), (121, 114), (116, 118), (119, 113), 
        (118, 116), (104, 125), (106, 126), (97, 137)  
    ]

    frames: list[IMG] = []
    for i in range(19):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 获取 locs 的位置和大小
        frame.paste(img, locs[i], alpha=True)      
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.1)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "doroqi",
    doroqi,
    min_images=1,
    max_images=1,
    keywords=["doro骑"],
    date_created=datetime(2025, 8, 6),
    date_modified=datetime(2025, 8, 6),
)
