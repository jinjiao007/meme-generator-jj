from datetime import datetime
from pathlib import Path
from math import pi

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def chuangfei(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((100, 100))  # 用户头像
    img_width, img_height = img.size  # 获取头像的宽度和高度
    center_x, center_y = img_width // 2, img_height // 2  # 头像的中心点

    # 计算每帧的旋转角度和移动位置
    frames = []
    for i in range(35):  # 总共35帧
        frame = BuildImage.open(img_dir / f"{i}.png")
        if i < 6:
            # 前6帧：头像固定在(77, 54)，不旋转
            paste_x, paste_y = 77, 54
            rotated_img = img
        elif i < 20:
            # 第6帧到第19帧：头像逆时针旋转并逐渐向左上角移动
            # 计算旋转角度（每帧增加30°）
            angle = -30 * (i - 5)  # 逆时针旋转
            # 计算移动位置（逐渐向左上角移动）
            move_distance = 5 * (i - 5)  # 每帧移动的距离
            paste_x = 77 - move_distance
            paste_y = 54 - move_distance
            # 旋转头像
            rotated_img = img.rotate(angle, center=(center_x, center_y), expand=True)
        else:
            # 第20帧及以后：头像完全移出画布
            paste_x, paste_y = -100, -100  # 将头像移出画布
            rotated_img = img

        # 确保头像粘贴位置正确
        paste_x = paste_x - (rotated_img.width - img_width) // 2
        paste_y = paste_y - (rotated_img.height - img_height) // 2

        frame.paste(rotated_img, (paste_x, paste_y), alpha=True)
        frames.append(frame.image)

    return save_gif(frames, 0.08)


add_meme(
    "chuangfei",
    chuangfei,
    min_images=1,
    max_images=1,
    keywords=["创飞"],
    date_created=datetime(2025, 5, 15),
    date_modified=datetime(2025, 5, 15),
)