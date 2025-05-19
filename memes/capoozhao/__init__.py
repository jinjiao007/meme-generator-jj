from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, ParserArg, ParserOption

img_dir = Path(__file__).parent / "images"


def capoozhao(images: list[BuildImage], texts: list[str], args):
    try:
        if not images:
            raise ValueError("No images provided")
        
        # 获取用户头像并转换为圆形
        img1 = images[0].convert("RGBA").circle().resize((38, 80))
        img2 = images[0].convert("RGBA").circle().resize((62, 68))

        # 帧位置定义
        head_locs_1 = [(31, 144), (25, 140), (25, 140), (25, 140)]  # 1-3帧的坐标
        head_locs_2 = [(20, 137), (20, 137), (20, 137)]  # 4-6帧的坐标

        # 处理文本
        if not texts:
            raise ValueError("No text provided")
        text = f"{texts[0]}"
        text2image = Text2Image.from_text(
            text, 35, fill=(0, 0, 0), stroke_width=3, stroke_fill="white",
            font_families=["033-SSFangTangTi"]
        ).wrap(440)
        if text2image.height > 500:
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "0.png")  # 打开背景图
        for i in range(7):
            frame = BuildImage.new("RGBA", (background.width, background.height))
            # 粘贴 images 中的 0-6.png
            png_img = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png_img, alpha=True)
            # 1-3帧粘贴第一张头像
            if 0 <= i <= 3:
                if i - 0 < len(head_locs_1):
                    frame.paste(img1, head_locs_1[i - 0], alpha=True)
            # 4-6帧粘贴第二张头像
            elif 4 <= i <= 6:
                if i - 4 < len(head_locs_2):
                    frame.paste(img2, head_locs_2[i - 4], alpha=True)
            # 粘贴文本 - 居中对齐
            text_w, _ = text_img.size
            x = (frame.width - text_w) // 2  # 居中对齐的x坐标
            frame.paste(text_img, (x, 266), alpha=True)
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.08)  # 前6帧每帧0.08秒，最后一帧1秒

    except Exception as e:
        print(f"Error generating meme: {e}")
        return BytesIO()


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    if not frames:
        return BytesIO()

    # 为前6帧设置相同的时长，最后一帧设置为1秒（1000毫秒）
    durations = [int(duration * 1000)] * (len(frames) - 1) + [1000]

    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,  # 使用自定义时长列表
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer


add_meme(
    "capoozhao",
    capoozhao,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["美死了"],
    keywords=["咖波照"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)
