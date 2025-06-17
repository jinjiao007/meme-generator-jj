from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def richu(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((80, 80)) # 将用户头像转换为圆形
    
    # 0-17帧中头像的位置和大小
    locs = [
        (78, 104), (82, 105), (84, 102), (89, 97), (91, 90),
        (94, 82), (98, 76), (102, 69), (104, 65), (106, 60),
        (107, 58), (107, 58)   
    ]

    frames: list[IMG] = []
    for i in range(12):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 获取 locs 的位置和大小
        frame.paste(img, locs[i], alpha=True)      
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.1)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "richu",
    richu,
    min_images=1,
    max_images=1,
    keywords=["日出"],
    date_created=datetime(2025, 6, 17),
    date_modified=datetime(2025, 6, 17),
)
