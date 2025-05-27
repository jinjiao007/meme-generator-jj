from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def spike_spinebuster(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((50, 45))  # 将用户头像转换为圆形
    
    # 0-9帧中头像的位置
    one_locs = [
        (203, 22), (180, 18), (219, 25), (219, 25), (247, 31), (246, 31), (259, 36),
        (265, 36), (265, 37), (164, 41)
    ]
    # 28-61帧坐标位置
    tow_locs = [
        (184, 11), (274, 13), (305, -10), (305, -10), (305, -10), (149, 21), (176, 161),
        (147, 189), (139, 173), (138, 172), (147, 137), (142, 99), (139, 95), (139, 95),
        (138, 87), (136, 88), (135, 76), (133, 76), (134, 84), (132, 92), (133, 114),
        (135, 157), (136, 161), (136, 161), (136, 161), (136, 161), (136, 161), (136, 161),
        (136, 161), (136, 161), (136, 161), (136, 161), (136, 161), (136, 161)
    ]
    frames: list[IMG] = []
    for i in range(61):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        
        # 粘贴背景图
        frame.paste(bg, alpha=True)
        
        # 获取 one_locs 的位置
        if i < len(one_locs):
            frame.paste(img, one_locs[i], alpha=True)
        # 获取 tow_locs 的位置
        if 27 <= i <= 61:
            if i - 27 < len(tow_locs):
                frame.paste(img, tow_locs[i - 27], alpha=True)
        
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.05)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "spike_spinebuster",
    spike_spinebuster,
    min_images=1,
    max_images=1,
    keywords=["斯派克抱摔"],
    date_created=datetime(2025, 5, 27),
    date_modified=datetime(2025, 5, 27),
)