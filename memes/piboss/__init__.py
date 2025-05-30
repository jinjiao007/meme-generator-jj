from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def piboss(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    
    # 0-2帧中头像的位置和大小
    locs = [
        (96, 104, 90, 190), (79, 118, 110, 170), (91, 97, 100, 190)
    ]

    frames: list[IMG] = []
    for i in range(3):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        
        # 获取 locs 的位置和大小
        x, y, w, h = locs[i]
        
        # 先调整头像大小再进行旋转
        resized_img = img.resize((w, h))
        rotated_img = resized_img.rotate(-10, expand=True)  # 逆时针旋转15°, expand=True保证旋转后图片完整
        
        # 计算旋转后图片的尺寸变化，以保证粘贴位置的准确性
        # 这里假设旋转不会显著改变图片尺寸，因此使用相同的x和y坐标
        # 如果需要精确计算，可以使用如下方法：
        new_w, new_h = rotated_img.size
        new_x = x - (new_w - w) // 2
        new_y = y - (new_h - h) // 2
        
        frame.paste(rotated_img, (new_x, new_y), alpha=True)
        
        # 粘贴背景图
        frame.paste(bg, alpha=True)
        
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "piboss",
    piboss,
    min_images=1,
    max_images=1,
    keywords=["痞老板"],
    date_created=datetime(2025, 5, 30),
    date_modified=datetime(2025, 5, 30),
)