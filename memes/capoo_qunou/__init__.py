from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_qunou(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    
    # 0-17帧中头像的位置和大小
    locs = [
        (126, 94, 120, 120), (126, 94, 120, 120), (128, 110, 110, 100), (140, 110, 110, 100), (126, 94, 120, 120),
        (126, 94, 120, 120), (126, 94, 120, 120), (126, 94, 120, 120), (128, 110, 110, 100), (128, 110, 110, 100),
        (126, 94, 120, 120), (126, 94, 120, 120), (126, 94, 120, 120), (126, 94, 120, 120), (128, 110, 110, 100),
        (128, 110, 110, 100), (126, 94, 120, 120), (126, 94, 120, 120)    
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
    "capoo_qunou",
    capoo_qunou,
    min_images=1,
    max_images=1,
    keywords=["咖波群殴"],
    date_created=datetime(2025, 6, 6),
    date_modified=datetime(2025, 6, 6),
)