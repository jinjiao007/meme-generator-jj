from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def onepunch(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((218, 211))
    # 获取背景图的尺寸
    background = BuildImage.open(img_dir / "0.png")
    bg_width, bg_height = background.width, background.height

    frames = []
    for i in range(8):
        # 创建透明背景图
        frame = BuildImage.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
        # 粘贴用户头像
        if 4 <= i <= 7:
            # 第4到第7帧：缩小头像并粘贴到(10, 10)
            resized_img = img.resize((img.width - 10, img.height - 10))
            frame.paste(resized_img, (10, 10), alpha=True)
        else:
            # 其他帧：正常粘贴头像到(0, 0)
            frame.paste(img, (0, 0), alpha=True)
        # 粘贴背景图
        bg = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(bg, (0, 0), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.02)


add_meme(
    "onepunch",
    onepunch,
    min_images=1,
    max_images=1,
    keywords=["给你一拳"],
    date_created=datetime(2025, 5, 16),
    date_modified=datetime(2025, 5, 16),
)