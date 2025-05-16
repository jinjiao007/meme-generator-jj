from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def spinner(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    frames: list[IMG] = []
    for i in range(24):  # 遍历24帧背景图片
        frame = BuildImage.open(img_dir / f"{i}.png")
        # 每帧头像顺时针旋转90°
        rotated_img = img.rotate(-90 * i, expand=True).circle().resize((74, 74))
        # 将旋转后的头像粘贴到指定位置(150,100)
        frame.paste(rotated_img, (150, 100), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "spinner",
    spinner,
    min_images=1,
    max_images=1,
    keywords=["陀螺"],
    date_created=datetime(2025, 5, 13),
    date_modified=datetime(2025, 5, 13),
)