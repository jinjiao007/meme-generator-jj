from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_love(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    
    # 0-17帧中头像的位置和大小
    locs = [
        (62, 133, 62, 62), (62, 133, 62, 62), (62, 133, 62, 62), (62, 133, 62, 62), (62, 133, 62, 62),
        (62, 133, 62, 62), (-62, -62, 62, 62), (-62, -62, 62, 62), (-62, -62, 62, 62), (-62, -62, 62, 62),
        (-62, -62, 62, 62), (85, 91, 45, 40), (73, 96, 45, 40), (61, 131, 65, 65)
    ]

    frames: list[IMG] = []
    for i in range(14):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        x,y,w,h = locs[i]
        # 获取 locs 的位置和大小
        frame.paste(img.resize((w, h)), (x, y), alpha=True)      
        # 粘贴背景图
        frame.paste(bg, alpha=True)       
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.08)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "capoo_love",
    capoo_love,
    min_images=1,
    max_images=1,
    keywords=["咖波爱心","❤️"],
    date_created=datetime(2025, 6, 6),
    date_modified=datetime(2025, 6, 6),
)