from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def zzdd(images: list[BuildImage], texts, args):

    img = images[0].convert("RGBA").resize((80, 80))  # 获取用户头像
    # 帧位置定义
    locs = [
        (47, 63), (47, 63), (47, 63), (47, 63), (51, 126), (51, 126),
        (51, 126), (51, 126), (51, 126), (39, 105), (39, 105), (39, 105),
        (39, 105), (39, 105), (47, 63)
        ]


    # 创建动态帧
    frames: list[IMG] = []
    background = BuildImage.open(img_dir / "0.png")  # 打开背景图
    for i in range(15):
        frame = BuildImage.new("RGBA", (background.width, background.height))
        png_img = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frame.paste(png_img, alpha=True)        
        frames.append(frame.image)

    # 返回 GIF 动画
    return save_gif(frames, 0.04) 



add_meme(
    "zzdd",
    zzdd,
    min_images=1,
    max_images=1,
    keywords=["指指点点"],
    date_created=datetime(2025, 7, 3),
    date_modified=datetime(2025, 7, 3),
)