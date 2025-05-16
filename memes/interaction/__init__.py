from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def fencing(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((100, 90))
    user_head = images[1].convert("RGBA").circle().resize((100, 90))
    
    # 获取第一张背景图的尺寸
    background = BuildImage.open(img_dir / "0.png")
    bg_width, bg_height = background.width, background.height
    
    # fmt: off
    user_locs = [
        (156, 90), (156, 86), (156, 90), (156, 86), (156, 93), (156, 103),
        (156, 93), (156, 103), (156, 93), (69, 103), (31, 103), (25, 103),
        (25, 103)
    ]
    self_locs = [
        (17, 90), (17, 83), (17, 90), (17, 83), (17, 102), (17, 93),
        (17, 102), (17, 93), (17, 102), (115, 93), (140, 93), (146, 93),
        (146, 93)
    ]
    # fmt: on
    
    frames: list[IMG] = []
    for i in range(13):
        # 创建一个空白背景图
        base_frame = BuildImage.new("RGBA", (bg_width, bg_height))
        # 粘贴用户头像和自己的头像到空白背景图上
        base_frame.paste(user_head, user_locs[i], alpha=True)
        base_frame.paste(self_head, self_locs[i], alpha=True)
        # 加载实际的背景图并粘贴到包含头像的空白背景图上
        current_background = BuildImage.open(img_dir / f"{i}.png")
        base_frame.paste(current_background, (0, 0), alpha=True)
        frames.append(base_frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "interaction",
    fencing,
    min_images=2,
    max_images=2,
    keywords=["互动"],
    date_created=datetime(2025, 5, 12),
    date_modified=datetime(2025, 5, 12),
)
