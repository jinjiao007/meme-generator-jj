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
        (-60, 0,1,1),(106, 137,18,13), (114, 100,26,31), (94, 0,68,83), (79, -10,69,65), (87, 2,62,58),
        (100, 2,64,66), (87, 1,62,64), (85, -6,65,66), (90, 0,60,64), (91, 2,58,57),(88, 0,61,62),
        (94, 1,60,60),(90, 2,58,57), (90, 2,58,57), (96, 6,56,58), (106, 14,69,65), (106, 35,62,58),
        (106, 48,64,66), (101, 54,62,64), (95, 52,65,66), (89, 46,61,62), (87, 48,61,62),(87, 48,61,62),
        (87, 48,61,62),(87, 48,61,62), (87, 48,61,62), (88, 49,61,62), (87, 51,61,62), (87, 53,61,62),
        (87, 50,61,62), (83, 44,61,62), (79, 41,61,62), (80, 44,61,62), (82, 47,61,62),(83, 48,61,62),
    ]

    rotate_num = [
        0, 0, -5, -10, 25, 20, -20, -12, 25, -15,
        0, 5, -5, 0, 0, 0, -2, 0, 0, -5, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
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
