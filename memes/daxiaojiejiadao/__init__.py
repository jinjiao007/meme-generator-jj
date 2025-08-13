from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image

from meme_generator.exception import TextOverLength
from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def daxiaojiejiadao(images: list[BuildImage], texts: list[str], args):
    img = images[0].convert("RGBA").circle().resize((100, 100))  # 将用户头像转换为圆形
    
    # 处理文本
    if not texts:
        raise ValueError("No text provided")
    text = f"{texts[0]}"
    text2image = Text2Image.from_text(
         text, 24, fill=(0, 0, 0), stroke_width=0.2, stroke_fill="#d6e5fc", font_families=["System"]
    ).wrap(327)
    if text2image.height > 45:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    # 0-14帧中头像的位置
    one_locs = [
        (144, 18, 27, 32), (144, 15, 27, 32), (141, 12, 27, 32), (139, 10, 27, 37), (131, 10, 31, 39),
        (146, 10, 31, 39), (146, 0, 33, 46), (108, -8, 34, 43), (101, -7, 34, 43), (102, -8, 39, 45),
        (96, 0, 41, 49), (113, 18, 37, 50), (118, 23, 37, 50), (161, 31, 36, 43), (153, 28, 36, 43),
        
    ]
  
    frames: list[IMG] = []
    for i in range(15):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        # 粘贴背景图
        frame.paste(bg, alpha=True)        
        # 获取 one_locs 的位置和大小
        x, y, w, h = one_locs[i]
        resized_img = img.resize((w, h))
        frame.paste(resized_img, (x, y), alpha=True)
        # 粘贴文本 - 居中对齐
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(text_img, (x, 200), alpha=True)
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.12)  # 保存为 GIF，帧间隔 0.05 秒


add_meme(
    "daxiaojiejiadao",
    daxiaojiejiadao,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["通通闪开，大小姐驾到！"],
    keywords=["大小姐驾到"],
    date_created=datetime(2025, 8, 13),
    date_modified=datetime(2025, 8, 13),
)