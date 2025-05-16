from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def slipper(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((74, 74))  # 用户头像
    frames: list[IMG] = []
    for i in range(16):  # 遍历16帧
        # 使用ditu.png作为背景
        frame = BuildImage.open(img_dir / "ditu.png").copy()
        # 粘贴用户头像
        if i >= 2:
            # 头像顺时针旋转100°
            rotated_img = img.rotate(-100 * (i - 2), expand=True)
            # 头像向左下角移动
            paste_x = 20 - 8 * (i - 2)
            paste_y = 120 + 10 * (i - 2)
        else:
            # 前2帧头像不旋转，位置固定
            rotated_img = img
            paste_x, paste_y = 20, 120
        frame.paste(rotated_img, (paste_x, paste_y), alpha=True)
        # 再粘贴0-15.png到背景上
        if i <= 15:
            overlay = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(overlay, (0, 0), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "slipper",
    slipper,
    min_images=1,
    max_images=1,
    keywords=["拖鞋"],
    date_created=datetime(2025, 5, 13),
    date_modified=datetime(2025, 5, 13),
)