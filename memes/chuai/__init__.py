from datetime import datetime
from pathlib import Path
import random  # 导入随机模块

from PIL.Image import Image as IMG
from pil_utils import BuildImage
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"
img1_dir = Path(__file__).parent / "images1"

def chuai(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((80, 80))

    locs = [
        (14, 220), (14, 220), (14, 220), (14, 220),
        (14, 220), (14, 220), (14, 220), (14, 220),
        (14, 220), (14, 220), (14, 220), (14, 220),
        (14, 220), (14, 220), (14, 220), (14, 220),
        (12, 220), (10, 220), (5, 220), (10, 220),
        (14, 220), (14, 220)
    ]

    frames: list[IMG] = []
    
    # 随机选择一个文件夹作为背景图源
    bg_folder = random.choice([img_dir, img1_dir])
    
    # 使用选定的文件夹中的所有图片
    for i in range(22):
        # 加载背景帧
        bg_frame = BuildImage.open(bg_folder / f"{i}.png")
        
        # 创建新帧
        frame = BuildImage.new("RGBA", bg_frame.size)
        frame.paste(bg_frame, alpha=True)
        
        # 添加用户头像
        frame.paste(img, locs[i], alpha=True)
        
        frames.append(frame.image)

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
