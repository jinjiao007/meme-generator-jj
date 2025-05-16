from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def play_baseball(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((66, 66))  # 用户头像
    img_width, img_height = img.size  # 获取头像的宽度和高度
    center_x, center_y = img_width // 2, img_height // 2  # 计算头像的中心点

    # 定义关键帧的x轴坐标
    key_frames = {
        0: 173,    # 第0帧x轴173
        8: 235,    # 第8帧x轴235
        16: 85,    # 第16帧x轴85
        22: 173    # 第22帧x轴173
    }

    # 计算每帧的x轴坐标
    locs = []
    for i in range(23):  # 总共23帧
        if i in key_frames:
            locs.append((key_frames[i], 87))
        else:
            # 找到前一个和后一个关键帧
            prev_key = max(k for k in key_frames if k < i)
            next_key = min(k for k in key_frames if k > i)
            # 计算x轴坐标的插值
            x = key_frames[prev_key] + int((key_frames[next_key] - key_frames[prev_key]) * (i - prev_key) / (next_key - prev_key))
            locs.append((x, 87))

    frames: list[IMG] = []
    current_angle = 0  # 当前旋转角度
    for i in range(23):
        frame = BuildImage.open(img_dir / f"{i}.png")
        if i <= 8:
            # 0-8帧：顺时针旋转90°（累计旋转角度）
            current_angle -= 90
        elif 9 <= i <= 16:
            # 9-16帧：逆时针旋转90°（累计旋转角度）
            current_angle += 90
        else:
            # 17-22帧：顺时针旋转90°（累计旋转角度）
            current_angle -= 90
        # 以头像中心点为中心旋转
        rotated_img = img.rotate(current_angle, center=(center_x, center_y), expand=True)
        # 计算旋转后头像的新位置，以确保头像的中心点对齐到指定坐标
        new_x = locs[i][0] - (rotated_img.width - img_width) // 2
        new_y = locs[i][1] - (rotated_img.height - img_height) // 2
        frame.paste(rotated_img, (new_x, new_y), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "play_baseball",
    play_baseball,
    min_images=1,
    max_images=1,
    keywords=["打棒球"],
    date_created=datetime(2025, 5, 15),
    date_modified=datetime(2025, 5, 15),
)