from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def dorochui(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle()
    user_head = images[1].convert("RGBA").circle()
    
    # 获取第一张背景图的尺寸
    background = BuildImage.open(img_dir / "0.png")
    bg_width, bg_height = background.width, background.height
    
    # fmt: off
    user_locs = [
        (73, 72, 120, 90), (117, 48, 120, 90)
    ]
    self_locs = [
        (19, 197, 100, 65), (1, 157, 120, 90)
    ]
    # fmt: on

    frames: list[IMG] = []
    for i in range(2):
        x1,y1,w1,h1 = user_locs[i]
        x2,y2,w2,h2 = self_locs[i]
        # 创建一个空白背景图
        base_frame = BuildImage.new("RGBA", (bg_width, bg_height))
        # 粘贴用户头像和自己的头像到空白背景图上
        base_frame.paste(self_head.resize((w1, h1)), (x1, y1), alpha=True)
        base_frame.paste(user_head.resize((w2, h2)), (x2, y2), alpha=True)
        # 加载实际的背景图并粘贴到包含头像的空白背景图上
        current_background = BuildImage.open(img_dir / f"{i}.png")
        base_frame.paste(current_background, (0, 0), alpha=True)
        frames.append(base_frame.image)
    return save_gif(frames, 0.02)


add_meme(
    "dorochui",
    dorochui,
    min_images=2,
    max_images=2,
    keywords=["doro锤"],
    date_created=datetime(2025, 6, 9),
    date_modified=datetime(2025, 6, 9),
)
