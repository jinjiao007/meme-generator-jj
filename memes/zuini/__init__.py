from datetime import datetime
from pathlib import Path

from PIL import Image
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def zuini(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()  # 将用户头像转换为方形
    # 从 args 中解析透明度参数，范围 0-255，默认值为 40（半透明）
    opacity = getattr(args, "opacity", 80)  # 使用 getattr 来安全地获取属性值
    opacity = max(0, min(255, opacity))  # 确保透明度在有效范围内
    # 转换为 PIL.Image.Image 对象，以便进行透明度调整
    img_pil = img.image
    # 确保图像有 alpha 通道
    if img_pil.mode != "RGBA":
        img_pil = img_pil.convert("RGBA")
    # 设置透明度：创建一个新的 alpha 通道，并应用透明度
    alpha = Image.new("L", img_pil.size, opacity)
    img_pil.putalpha(alpha)
    # 0-9帧中头像的位置
    one_locs = [
        (-5, -5, 260, 260), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240),
        (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240),
        (-5, -5, 260, 260), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240),
        (0, 0, 240, 240), (0, 0, 240, 240), (-5, -5, 260, 260), (0, 0, 240, 240), (0, 0, 240, 240),
        (0, 0, 240, 240), (0, 0, 240, 240), (0, 0, 240, 240)
    ]
  
    frames = []
    for i in range(23):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 粘贴背景图
        frame.paste(bg, alpha=True)        
        # 获取 one_locs 的位置和大小
        x, y, w, h = one_locs[i]
        resized_img_pil = img_pil.resize((w, h))
        # 转换为 BuildImage 对象以便粘贴
        resized_img = BuildImage(resized_img_pil)
        frame.paste(resized_img, (x, y), alpha=True)  # 粘贴透明化处理后的头像
        
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.04)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "zuini",
    zuini,
    min_images=1,
    max_images=1,
    keywords=["嘴你"],
    date_created=datetime(2025, 6, 11),
    date_modified=datetime(2025, 6, 11),
)
