from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def doroti(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    
    # 0-11帧中头像的位置和大小
    locs = [
        (33, 124, 70, 62), (30, 122, 70, 62), (30, 122, 70, 62), (30, 122, 70, 62), 
        (30, 122, 70, 62), (30, 122, 70, 62), (30, 122, 70, 62), (30, 122, 70, 62),
        (30, 122, 70, 62), (30, 122, 70, 62)
    ]
    # 11-14帧坐标位置和大小
    tow_locs = [
        (28, 132, 62, 55), (24, 111, 62, 55), (-12, 64, 62, 55), (-51, 43, 62, 55)
    ]
    frames: list[IMG] = []
    for i in range(19):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 获取 locs 的位置和大小
        if i < len(locs):
            x1, y1, w1, h1 = locs[i]
            frame.paste(img.resize((w1, h1)), (x1, y1), alpha=True)
        # 获取 tow_locs 的位置和大小
        if 10 <= i <= 14:
            if i - 10 < len(tow_locs):
                x2, y2, w2, h2 = tow_locs[i - 10]
                frame.paste(img.resize((w2, h2)), (x2, y2), alpha=True)        
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "doroti",
    doroti,
    min_images=1,
    max_images=1,
    keywords=["doro踢"],
    date_created=datetime(2025, 5, 27),
    date_modified=datetime(2025, 5, 27),
)