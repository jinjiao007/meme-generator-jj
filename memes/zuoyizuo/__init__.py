from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def zuoyizuo(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()  # 将用户头像转换为圆形
    
    # 0-17帧中头像的位置和大小
    locs = [
        (78, 140, 95, 100), (76, 130, 100, 110), (76, 140, 100, 110), (78, 140, 95, 100), (76, 130, 100, 110),
        (76, 130, 100, 110), (78, 140, 95, 100), (78, 140, 95, 100), (76, 130, 100, 110), (75, 130, 100, 110),
        (76, 130, 100, 110), (75, 130, 100, 110), (76, 130, 100, 110), (76, 130, 100, 110), (75, 130, 100, 110),
        (78, 130, 95, 100), (78, 140, 95, 100), (78, 140, 95, 100)    
    ]

    frames: list[IMG] = []
    for i in range(18):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        x,y,w,h = locs[i]
        # 获取 locs 的位置和大小
        frame.paste(img.resize((w, h)), (x, y), alpha=True)      
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "zuoyizuo",
    zuoyizuo,
    min_images=1,
    max_images=1,
    keywords=["唑一唑"],
    date_created=datetime(2025, 6, 17),
    date_modified=datetime(2025, 6, 17),
)