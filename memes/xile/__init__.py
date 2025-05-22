from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def xile(images: list[BuildImage], texts: list[str], args):
    try:
        if not images:
            raise ValueError("No images provided")
        
        # 获取用户头像并转换为圆形
        img = images[0].convert("RGBA").circle().resize((200, 200))

        # 获取头像中点
        center_x = img.width // 2
        center_y = img.height // 2

        # 处理文本
        if not texts:
            raise ValueError("No text provided")
        text = "救我，我要洗了"
        text2image = Text2Image.from_text(
            text, 35, fill=(0, 0, 0), stroke_width=0.2, stroke_fill="",
            font_families=["System"]
        ).wrap(440)
        if text2image.height > 500:
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "xiyiji.png")  # 打开背景图

        # 定义各帧的持续时间（秒）
        durations = [0.08] * 3 + [0.05] * 12 + [0.15] * 7

        for i in range(22):
            frame = BuildImage.new("RGBA", (background.width, background.height))           
            png_img = BuildImage.open(img_dir / "xiyiji.png")    
            frame.paste(png_img, alpha=True)       

            # 计算旋转角度（0-21帧逐帧旋转60°）
            angle = -60 * (i + 1)   # 顺时针旋转

            # 旋转头像
            rotated_img = img.rotate(angle, expand=True)
            # 计算粘贴位置以保持中点位置不变
            paste_x = 72 + center_x - rotated_img.width // 2
            paste_y = 97 + center_y - rotated_img.height // 2
            frame.paste(rotated_img, (paste_x, paste_y), alpha=True)

            # 粘贴文本 - 居中对齐
            text_w, _ = text_img.size
            x = (frame.width - text_w) // 2  # 居中对齐x的坐标
            frame.paste(text_img, (x, 16), alpha=True)
            
            frames.append(frame.image)

        # 返回 GIF 动画，设置各帧持续时间
        return save_gif(frames, durations)  

    except Exception as e:
        print(f"Error generating meme: {e}")
        return BytesIO()


def save_gif(frames: list[IMG], durations: list[float]) -> BytesIO:
    """将帧列表保存为GIF动画"""
    if not frames:
        return BytesIO()

    buffer = BytesIO()
    # 将持续时间从秒转换为毫秒
    durations_ms = [int(d * 1000) for d in durations]
    
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        disposal=2,
        duration=durations_ms
    )
    buffer.seek(0)
    return buffer


add_meme(
    "xile",
    xile,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["救我，我要洗了"],
    keywords=["洗了"],
    date_created=datetime(2025, 5, 21),
    date_modified=datetime(2025, 5, 21),
)
