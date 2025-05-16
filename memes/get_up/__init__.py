from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def get_up(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((100, 100))  # 用户头像
    img_width, img_height = img.size  # 获取头像的宽度和高度
    center_x, center_y = img_width // 2, img_height // 2  # 计算头像的中心点

    # fmt: off
    locs = [
        (7, 62), (9, 60), (9, 60), (9, 60), (9, 60), (9, 60), 
        (7, 62), (7, 62), (7, 62), (7, 62), (7, 62), (7, 62), 
        (7, 62), (7, 62), (7, 62), (7, 62), (7, 62), (7, 62), 
        (7, 62), (7, 62)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(20):
        frame = BuildImage.open(img_dir / f"{i}.png")
        # 以头像中心点为中心逆时针旋转45°
        rotated_img = img.rotate(45, center=(center_x, center_y), expand=True)
        # 计算旋转后头像的新位置，以确保头像的中心点对齐到指定坐标
        new_x = locs[i][0] - (rotated_img.width - img_width) // 2
        new_y = locs[i][1] - (rotated_img.height - img_height) // 2
        frame.paste(rotated_img, (new_x, new_y), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "get_up",
    get_up,
    min_images=1,
    max_images=1,
    keywords=["起床"],
    date_created=datetime(2025, 5, 14),
    date_modified=datetime(2025, 5, 14),
)