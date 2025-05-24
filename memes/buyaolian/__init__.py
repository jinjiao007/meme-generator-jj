from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.utils import save_gif
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

def buyaolian(images: list[BuildImage], texts: list[str], args):
    img = images[0].convert("RGBA").square()  # 将用户头像转换为方形
    
    text = f"{texts[0]}"
    text2image = Text2Image.from_text(
        text, 35, fill=(0, 0, 0), stroke_width=3, stroke_fill="white",
        font_families=["033-SSFangTangTi"]
    ).wrap(400)
    if text2image.height > 85:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    # 每帧中头像的位置和大小
    one_locs = [
        (130, 179, 93, 80), (130, 179, 93, 80), (137, 202, 94, 96), (152, 248, 95, 100),
        (188, 313, 69, 74)
    ]
    tow_locs = [
        (137, 85, 90, 82), (139, 111, 93, 80), (138, 172, 90, 91), (138, 172, 90, 91),
    ]
    frames: list[IMG] = []
    for i in range(6):
        bg = BuildImage.open(img_dir / f"{i}.png")  # 打开背景图
        frame = BuildImage.new("RGBA", bg.size, "white")  # 创建新帧
        
        # 获取 current_loc 的位置和大小
        if i < len(one_locs):
            x1, y1, w1, h1 = one_locs[i]
            frame.paste(img.resize((w1, h1)), (x1, y1), alpha=True)
        # 获取tow_loc的位置和大小
        if 1 <= i <=4:
            x2, y2, w2, h2 = tow_locs[i-1]  # 获取tow_locs对应位置的坐标
            frame.paste(img.resize((w2, h2)), (x2, y2), alpha=True)
        # 粘贴背景图
        frame.paste(bg, alpha=True)
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(text_img, (x, 18), alpha=True)
        frames.append(frame.image)  # 添加当前帧到帧列表
    
    return save_gif(frames, 0.1)  # 保存为GIF，帧间隔0.08秒


add_meme(
    "buyaolian",
    buyaolian,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["我就是不要脸\n 你来撕我啊"],
    keywords=["不要脸", "撕脸"],
    date_created=datetime(2025, 5, 24),
    date_modified=datetime(2025, 5, 24),
)