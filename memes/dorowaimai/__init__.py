from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def dorowaimai(images: list[BuildImage], texts: list[str], args):

    # 获取用户头像并创建副本用于旋转处理
    base_img = images[0].convert("RGBA").resize((40, 30))
    
    # 帧位置定义
    locs = [
        (29, 152), (29, 152), (29, 151), (29, 149), 
        (29, 153), (29, 153), (29, 151), (29, 149)
    ]

    # 处理文本
    text = f"{texts[0]}专送"
    text2image = Text2Image.from_text(
        text, 25, fill=(0, 0, 0), stroke_width=3, stroke_fill="white",
        font_families=["033-SSFangTangTi"]
        ).wrap(197)
    if text2image.height > 40:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    # 创建动态帧
    frames: list[IMG] = []
    background = BuildImage.open(img_dir / "0.png")  # 打开背景图
    for i in range(8):
        frame = BuildImage.new("RGBA", (background.width, background.height))
        png_img = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(png_img, alpha=True)
        
        # 复制并旋转头像（顺时针15度）
        img_rotated = base_img.copy().rotate(-15, expand=True, center=(20, 15))
        
        # 计算新位置确保中心点对齐
        center_x = locs[i][0] + 20  # 原始中心点X
        center_y = locs[i][1] + 15  # 原始中心点Y
        new_x = center_x - img_rotated.width // 2
        new_y = center_y - img_rotated.height // 2
        
        # 粘贴旋转后的头像
        frame.paste(img_rotated, (int(new_x), int(new_y)), alpha=True)
        
        # 粘贴文本 - 居中对齐
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(text_img, (x, 3), alpha=True)        
        frames.append(frame.image)

    # 返回 GIF 动画
    return save_gif(frames, 0.04) 



add_meme(
    "dorowaimai",
    dorowaimai,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["doro"],
    keywords=["doro外卖"],
    date_created=datetime(2025, 7, 4),
    date_modified=datetime(2025, 7, 4),
)