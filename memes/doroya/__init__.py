from datetime import datetime
from pathlib import Path
import numpy as np

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def doroya(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((150, 150))  # 用户头像

    # 定义旋转角度（顺时针为正，逆时针为负）
    rotate_angles = [0, -15, 5, 15, 30, 5]  # 1和2帧顺时针15°，3、4、5帧逆时针15°
    
    # 定义各帧的位置
    locs = [
        (124, 135), (124, 135), (124, 120), (105, 115), (83, 110), (100, 112)
    ]
    
    # 获取背景图片的大小
    background_size = BuildImage.open(img_dir / "0.png").size
    
    frames: list[IMG] = []
    for i in range(6):
        # 创建透明背景图
        transparent_background = BuildImage.new("RGBA", background_size, (0, 0, 0, 0))
        
        # 旋转头像
        rotated_img = img.rotate(rotate_angles[i] if i < len(rotate_angles) else 0, expand=True)
        
        # 将旋转后的头像粘贴到透明背景图的指定位置
        transparent_background.paste(rotated_img, locs[i % len(locs)], alpha=True)
        
        # 打开背景图片并粘贴到透明背景图上
        background = BuildImage.open(img_dir / f"{i}.png")
        transparent_background.paste(background, alpha=True)
        
        frames.append(transparent_background.image)
    
    return save_gif(frames, 0.08)


add_meme(
    "doroya",
    doroya,
    min_images=1,
    max_images=1,
    keywords=["doro鸭"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)