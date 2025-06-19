from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"

def liedui(images: list[BuildImage], texts, args):
    # 打开背景图作为画布
    frame = BuildImage.open(img_dir / "0.png")
    bg_width, bg_height = frame.size
    
    # 获取用户头像并转为RGBA
    user_img = images[0].convert("RGBA")
    
    # 初始位置和尺寸
    x_position = 0
    size = 1  # 初始头像尺寸
    
    # 循环粘贴头像直到到达背景图最右边
    while x_position < bg_width:
        # 调整头像大小
        current_img = user_img.resize((size, size), keep_ratio=True)
        
        # 粘贴到头像到背景图
        frame.paste(current_img, (int(x_position), 0), alpha=True)
        
        # 更新位置：x坐标增加当前头像宽度
        x_position += current_img.width - 10
        
        # 头像尺寸增加2像素
        size += 3
        
        # 如果头像高度已超过剩余空间，提前结束循环
        if x_position + size > bg_height + 500:
            break

    return frame.save_jpg()

add_meme(
    "liedui",
    liedui,
    min_images=1,
    max_images=1,
    keywords=["列队"],
    date_created=datetime(2025, 6, 19),
    date_modified=datetime(2025, 6, 19),
)