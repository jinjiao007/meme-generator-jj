from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def zuini(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()  # 将用户头像转换为方形
    # 创建一个与头像同尺寸的全白遮罩（表示完全不透明）
    mask = BuildImage.new("L", img.size, 25)  # 创建一个全白的遮罩图像，尺寸与头像一致
    mask = mask.image  # 获取底层的 PIL.Image.Image 对象
    # 0-9帧中头像的位置
    one_locs = [
        (-5, -5, 260, 260), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240),
        (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240),
        (-5, -5, 260, 260), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240),
        (0, 0, 240, 240), (0, 0, 240, 240), (-5, -5, 260, 260), (0, 0, 240, 240), (0, 0, 240, 240),
        (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240)
    ]
  
    frames: list[IMG] = []
    for i in range(23):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 粘贴背景图
        frame.paste(bg, alpha=True)        
        # 获取 one_locs 的位置和大小
        x, y, w, h = one_locs[i]
        resized_img = img.resize((w, h))
        resized_mask = mask.resize((w, h))  # 调整遮罩尺寸
        frame.image.paste(resized_img.image, (x, y), mask=resized_mask)  # 使用调整后的遮罩
        
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.02)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "zuini",
    zuini,
    min_images=1,
    max_images=1,
    keywords=["嘴你"],
    date_created=datetime(2025, 6, 11),
    date_modified=datetime(2025, 6, 11),
)