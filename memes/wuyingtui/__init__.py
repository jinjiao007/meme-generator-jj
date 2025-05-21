from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def wuyingtui(images: list[BuildImage], texts, args):
    try:
        if not images:
            raise ValueError("No images provided")
        
        # 获取用户头像
        img = images[0].convert("RGBA").resize((34, 34))

        # 帧位置定义
        locs= [(78, 70), (78, 70), (75, 72), (75, 72), (78, 70), (78, 70),
                (75, 72), (75, 72), (78, 70), (78, 70), (75, 72), (75, 72),
                (78, 70), (78, 70), (78, 70), (78, 70), (75, 72), (75, 72)
                ]


        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "0.png")  # 打开背景图
        for i in range(18):
            frame = BuildImage.new("RGBA", (background.width, background.height))                     
            frame.paste(img, locs[i], alpha=True)
            png_img = BuildImage.open(img_dir / f"{i}.png")    
            frame.paste(png_img, alpha=True)       
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.08)  

    except Exception as e:
        print(f"Error generating meme: {e}")
        return BytesIO()


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    if not frames:
        return BytesIO()


    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer


add_meme(
    "wuyingtui",
    wuyingtui,
    min_images=1,
    max_images=1,
    keywords=["无影腿"],
    date_created=datetime(2025, 5, 21),
    date_modified=datetime(2025, 5, 21),
)