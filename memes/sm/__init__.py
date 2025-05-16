from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def sm(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((74, 74))  # 用户头像
    frames: list[IMG] = []
    for i in range(20):
        # 创建透明背景图
        frame = BuildImage.new("RGBA", (200, 200), (0, 0, 0, 0))
        # 前9帧头像不旋转
        if i < 9:
            frame.paste(img, (125, 88), alpha=True)
        # 第10-20帧头像逆时针旋转30°
        else:
            rotated_img = img.rotate(30, expand=True)
            frame.paste(rotated_img, (125, 88), alpha=True)
        # 粘贴背景图
        overlay = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(overlay, (0, 0), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "sm",
    sm,
    min_images=1,
    max_images=1,
    keywords=["sm"],
    date_created=datetime(2025, 5, 13),
    date_modified=datetime(2025, 5, 13),
)