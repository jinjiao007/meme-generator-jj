from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def pinailong(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((100, 100))  # 将用户头像转换为圆形
    
    # 0-9帧中头像的位置
    one_locs = [
        (91, 60, 100, 100), (158, 89, 100, 100), (154, 64, 90, 90), (172, 76, 90, 90), (186, 76, 90, 88),
        (179, 114, 90, 88), (85, 36, 85, 85), (93, 44, 85, 85), (93, 107, 85, 85), (70, 132, 85, 85),
        (90, 102, 85, 85), (99, 94, 95, 85), (93, 87, 110, 100), (61, 72, 140, 130), (40, 62, 150, 145),
        (-20, 93, 180, 160), (54, 75, 150, 150), (62, 59, 155, 140), (60, 55, 155, 140), (73, 51, 148, 140),
        (69, 55, 145, 140), (72, 50, 145, 140), (68, 52, 145, 140), (68, 52, 145, 140)
    ]
  
    frames: list[IMG] = []
    for i in range(24):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 粘贴背景图
        frame.paste(bg, alpha=True)        
        # 获取 one_locs 的位置和大小
        x, y, w, h = one_locs[i]
        resized_img = img.resize((w, h))
        frame.paste(resized_img, (x, y), alpha=True)
        
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.12)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "pinailong",
    pinailong,
    min_images=1,
    max_images=1,
    keywords=["劈奶龙"],
    date_created=datetime(2025, 5, 31),
    date_modified=datetime(2025, 5, 31),
)