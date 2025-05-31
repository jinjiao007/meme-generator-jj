from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def penshe(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()  # 将用户头像转换为圆形
    #one_locs=[(118, 108, 188, 145)]
    # 11-15帧头像的位置
    tow_locs = [
        (48, 45, 102, 81), (30, 34, 80, 81), (19, 17, 74, 75), (18, 11, 59, 60), (-19, -21, 52, 52)
    ]
    frames: list[IMG] = []
    for i in range(15):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧       
        
        # 获取 one_locs 的位置和大小
        if i < 10:
            x1, y1, w1, h1 = (25, 25, 188, 155)
            # 先调整头像大小再进行旋转
            resized_img = img.resize((w1, h1))
            rotated_img = resized_img.rotate(43, expand=True)  # 逆时针旋转180°
            # 计算旋转后图片的尺寸变化，以保证粘贴位置的准确性
            new_w, new_h = rotated_img.size
            new_x = x1 - (new_w - w1) // 2
            new_y = y1 - (new_h - h1) // 2
            frame.paste(rotated_img, (new_x, new_y), alpha=True)
        
        # 获取 tow_locs 的位置和大小
        if 11 <= i <= 15:
            if i - 10 < len(tow_locs):
                x2, y2, w2, h2 = tow_locs[i - 10]
                resized_img = img.resize((w2, h2))
                rotated_img = resized_img.rotate(43, expand=True)  # 逆时针旋转15°
                # 计算旋转后图片的尺寸变化，以保证粘贴位置的准确性
                new_w2, new_h2 = rotated_img.size
                new_x2 = x2 - (new_w2 - w2) // 2
                new_y2 = y2 - (new_h2 - h2) // 2
                frame.paste(rotated_img, (new_x2, new_y2), alpha=True)
        # 粘贴背景图
        frame.paste(bg, alpha=True)
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.1)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "penshe",
    penshe,
    min_images=1,
    max_images=1,
    keywords=["喷射"],
    date_created=datetime(2025, 5, 31),
    date_modified=datetime(2025, 5, 31),
)