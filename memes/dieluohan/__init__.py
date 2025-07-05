from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

from pil_utils import BuildImage
from meme_generator import add_meme


def dieluohan(images: list[BuildImage], texts, args):
    # 创建200x400的透明背景图
    bg_img = BuildImage.new("RGBA", (200, 250), (0, 0, 0, 0))
    
    # 获取用户头像并转为RGBA
    user_img = images[0].convert("RGBA")
    
    # 椭圆尺寸
    ellipse_width = 180
    ellipse_height = 50
    
    # 创建椭圆遮罩
    mask = Image.new("L", (ellipse_width, ellipse_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, ellipse_width, ellipse_height), fill=255)
    
    # 初始位置
    x_position = 12
    y_position = 200
    
    # 循环粘贴头像直到到达顶部
    while y_position >= 0:
        # 创建椭圆头像
        # 1. 调整用户头像大小以填充椭圆
        avatar = user_img.resize(
            (ellipse_width, ellipse_height), 
            keep_ratio=False  # 不保持比例，拉伸填充
        ).image
        
        # 2. 应用椭圆遮罩
        ellipse_img = Image.new("RGBA", (ellipse_width, ellipse_height))
        ellipse_img.paste(avatar, (0, 0), mask)
        
        # 3. 转换为BuildImage对象
        ellipse_bgimg = BuildImage(ellipse_img)
        
        # 粘贴到头像到背景图
        bg_img.paste(ellipse_bgimg, (int(x_position), int(y_position)), alpha=True)
        
        y_position -= 10
        

    return bg_img.save_jpg()

add_meme(
    "dieluohan",
    dieluohan,
    min_images=1,
    max_images=1,
    keywords=["叠罗汉"],
    date_created=datetime(2025, 7, 5),
    date_modified=datetime(2025, 7, 5),
)