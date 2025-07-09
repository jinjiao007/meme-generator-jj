from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def sibalu(images: list[BuildImage], texts: list[str], args):
    try:
        img = images[0].convert("RGBA").resize((42, 93))  # 获取用户头像

        # 帧位置定义（从0到23帧的坐标）
        head_locs = [
            (-8, 118), (-8, 118), (-8, 118), (-8, 118), (-8, 118), (-8, 118),
            (-8, 118), (-8, 118), (-8, 118), (-8, 118), (-8, 118), (-5, 115),
            (-5, 112), (10, 112), (78, 108), (94, 107), (94, 107), (94, 107),
            (94, 107), (95, 109), (95, 109), (95, 109), (95, 109)
        ]
        rotate_num = [
            7,7,7,7,7,7,7,7,7,7,7,7,7,-6,-6, 4, 4, 4, 4, 4, 4, 4, 4, 
        ]

        # 处理文本
        if not texts:
            raise ValueError("No text provided")
        text = f"{texts[0]}"
        text2image = Text2Image.from_text(
            text, 20,fill=(0, 0, 0), stroke_width=3, stroke_fill="white",
            font_families=["033-SSFangTangTi"]
        ).wrap(200)
        if text2image.height > 30:
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "0.png")  # 打开背景图
        for i in range(31):
            frame = BuildImage.new("RGBA", (background.width, background.height))
            
            png_img = BuildImage.open(img_dir / f"{i}.png")
            # 0-22帧粘贴头像
            if i <= 22:
                # 旋转头像
                rotated_img = img.rotate(rotate_num[i], expand=True)
                # 粘贴旋转后的头像
                frame.paste(rotated_img, head_locs[i], alpha=True)
                
            frame.paste(png_img, (0, 0), alpha=True)  # 添加位置坐标 
            if i <= 22:
                # 粘贴文本 - 居中对齐
                text_w, _ = text_img.size
                x = (frame.width - text_w) // 2  # 居中对齐的x坐标
                frame.paste(text_img, (x, 182), alpha=True)          
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.08)  
    except Exception as e:
        # 在实际应用中，可能需要记录错误或重新抛出
        raise e


add_meme(
    "sibalu",
    sibalu,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["给你看个傻子"],
    keywords=["486"],
    date_created=datetime(2025, 7, 9),
    date_modified=datetime(2025, 7, 9),
)