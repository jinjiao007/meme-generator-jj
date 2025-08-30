from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def yuanshen(images: list[BuildImage], texts, args):
    user_head = images[0].convert("RGBA").resize((60,60))
    user_locs = [
        (-60, 0,1,1),(106, 137,18,13), (114, 100,26,31), (80, -5,75,89), (79, -10,75,80), (85, 2,62,55),
        (87, 2,68,68), (87, 1,68,64), (85, -4,70,72), (89, 0,65,66), (91, 2,58,57),(88, 0,64,62),
        (90, 1,62,60),(90, 2,58,57), (90, 2,58,57), (96, 6,56,58), (106, 14,69,65), (106, 35,62,58),
        (106, 48,64,66), (101, 54,62,64), (95, 52,65,66), (89, 46,61,62), (87, 48,61,62),(87, 48,61,62),
        (87, 48,61,62),(87, 48,61,62), (87, 48,61,62), (86, 49,61,62), (87, 51,61,62), (87, 53,61,62),
        (87, 50,61,62), (81, 44,61,62), (79, 39,61,62), (78, 42,61,62), (80, 45,61,62),(81, 46,61,62),
    ]

    rotate_num = [
        0, 0, -5, -15, 25, 22, -15, -6, 12, -7,
        0, 4, -3, 0, 0, 0, -1, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0
        ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(36):
        frame = BuildImage.open(img_dir / f"{i}.png")

        # 1. 旋转
        rotated = user_head.copy().rotate(rotate_num[i], expand=True)

        # 2. 取当前帧的目标宽高并缩放
        x, y, w, h = user_locs[i]
        resized = rotated.resize((w, h))

        # 3. 贴到对应位置
        frame.paste(resized, (x, y), alpha=True, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "yuanshen",
    yuanshen,
    min_images=1,
    max_images=1,
    keywords=["缘神"],
    date_created=datetime(2025, 8, 29),
    date_modified=datetime(2025, 8, 29),
)
