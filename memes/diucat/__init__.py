from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def diucat(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    
    # 0-9帧中头像的位置
    one_locs = [
        (95, 250, 80, 80), (101, 240, 80, 80), (102, 226, 80, 80), (99, 208, 80, 80), (94, 195, 80, 80),
        (80, 187, 80, 80), (82, 188, 60, 60), (65, 172, 60, 60), (53, 151, 60, 60)
    ]
    # 16-18帧头像的位置
    tow_locs = [
        (80, 34, 30, 30), (65, 45, 30, 30), (65, 45, 30, 30)
    ]
    frames: list[IMG] = []
    for i in range(27):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        
        # 粘贴背景图
        frame.paste(bg, alpha=True)
        
        # 获取 one_locs 的位置和大小
        if i < len(one_locs):
            x1, y1, w1, h1 = one_locs[i]
            # 先调整头像大小再进行旋转
            resized_img = img.resize((w1, h1))
            rotated_img = resized_img.rotate(-160, expand=True)  # 逆时针旋转180°
            # 计算旋转后图片的尺寸变化，以保证粘贴位置的准确性
            new_w, new_h = rotated_img.size
            new_x = x1 - (new_w - w1) // 2
            new_y = y1 - (new_h - h1) // 2
            frame.paste(rotated_img, (new_x, new_y), alpha=True)
        
        # 获取 tow_locs 的位置和大小
        if 16 <= i <= 18:
            if i - 16 < len(tow_locs):
                x2, y2, w2, h2 = tow_locs[i - 16]
                resized_img = img.resize((w2, h2))
                rotated_img = resized_img.rotate(15, expand=True)  # 逆时针旋转15°
                # 计算旋转后图片的尺寸变化，以保证粘贴位置的准确性
                new_w2, new_h2 = rotated_img.size
                new_x2 = x2 - (new_w2 - w2) // 2
                new_y2 = y2 - (new_h2 - h2) // 2
                frame.paste(rotated_img, (new_x2, new_y2), alpha=True)
        
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "diucat",
    diucat,
    min_images=1,
    max_images=1,
    keywords=["丢猫"],
    date_created=datetime(2025, 5, 30),
    date_modified=datetime(2025, 5, 30),
)