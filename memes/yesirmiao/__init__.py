from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def yesirmiao(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    
    # 0-10帧中头像的位置和大小
    locs = [
        (111, 48, 125, 110), (99, 42, 125, 110), (91, 43, 125, 110), (86, 43, 125, 110), 
        (79, 39, 125, 110), (71, 41, 125, 110), (62, 43, 125, 110), (56, 44, 125, 110),
        (47, 45, 125, 110), (37, 44, 125, 110)
    ]
    # 11-25帧坐标位置和大小
    tow_locs = [
        (25, 42, 125, 100), (13, 42, 125, 100), (6, 41, 125, 100), (4, 43, 125, 100),
        (5, 50, 125, 100), (6, 56, 125, 110), (11, 65, 125, 100), (16, 71, 125, 100),
        (24, 78, 125, 100), (33, 66, 125, 100), (37, 31, 125, 100), (44, 15, 125, 90),
        (47, 21, 125, 90), (54, 26, 125, 90), (56, 32, 125, 90)
    ]
    frames: list[IMG] = []
    for i in range(25):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 获取 locs 的位置和大小
        if i < len(locs):
            x1, y1, w1, h1 = locs[i]
            frame.paste(img.resize((w1, h1)), (x1, y1), alpha=True)
        # 获取 tow_locs 的位置和大小
        if 10 <= i <= 25:
            if i - 10 < len(tow_locs):
                x2, y2, w2, h2 = tow_locs[i - 10]
                frame.paste(img.resize((w2, h2)), (x2, y2), alpha=True)        
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "yesirmiao",
    yesirmiao,
    min_images=1,
    max_images=1,
    keywords=["敬礼喵"],
    date_created=datetime(2025, 5, 28),
    date_modified=datetime(2025, 5, 28),
)