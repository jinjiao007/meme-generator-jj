from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def turtle_jue(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((29, 29))
    user_head = images[1].convert("RGBA").circle().resize((29, 29))
    
    # 获取第一张背景图的尺寸
    background = BuildImage.open(img_dir / "0.png")
    bg_width, bg_height = background.width, background.height
    
    # fmt: off
    user_locs = [
        (3, 52), (2, 54), (-2, 54), (2, 54)
    ]
    self_locs = [
        (33, 16), (20, 18), (18, 14), (28, 16)
    ]
    # fmt: on
    
    frames: list[IMG] = []
    for i in range(4):
        # 创建一个空白背景图
        base_frame = BuildImage.new("RGBA", (bg_width, bg_height))
        
        # user 头像逆时针旋转 120°
        user_rotated = user_head.rotate(120, expand=True)
        # 计算旋转后头像的尺寸变化，确保头像中心对齐到指定坐标
        user_x = user_locs[i][0] - (user_rotated.width - user_head.width) // 2
        user_y = user_locs[i][1] - (user_rotated.height - user_head.height) // 2
        base_frame.paste(user_rotated, (user_x, user_y), alpha=True)
        
        # self 头像逆时针旋转 30°
        self_rotated = self_head.rotate(30, expand=True)
        # 计算旋转后头像的尺寸变化，确保头像中心对齐到指定坐标
        self_x = self_locs[i][0] - (self_rotated.width - self_head.width) // 2
        self_y = self_locs[i][1] - (self_rotated.height - self_head.height) // 2
        base_frame.paste(self_rotated, (self_x, self_y), alpha=True)
        
        # 加载实际的背景图并粘贴到包含头像的空白背景图上
        current_background = BuildImage.open(img_dir / f"{i}.png")
        base_frame.paste(current_background, (0, 0), alpha=True)
        
        frames.append(base_frame.image)
    return save_gif(frames, 0.02)


add_meme(
    "turtle_jue",
    turtle_jue,
    min_images=2,
    max_images=2,
    keywords=["龟龟撅"],
    date_created=datetime(2025, 5, 12),
    date_modified=datetime(2025, 5, 12),
)