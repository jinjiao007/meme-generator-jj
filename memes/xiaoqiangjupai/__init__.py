from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def xiaoqiangjupai(images: list[BuildImage], texts: list[str], args):
    try:
        if not texts:
            raise ValueError("No text provided")
        text = texts[0].strip()
        if not text:
            raise ValueError("Text cannot be empty after stripping spaces")

        # -------------------------- 调整：文本最大宽度 --------------------------
        # 定义文本渲染的最大区域（宽181，高150）
        TEXT_MAX_WIDTH = 181  
        TEXT_MAX_HEIGHT = 150
        max_font_size = 50  # 最大字号
        min_font_size = 10  # 最小字号
        optimal_font_size = min_font_size  # 初始化最优字号为最小值

        # 从最大字号向下试探，找到能放入区域的最大字号
        for font_size in range(max_font_size, min_font_size - 1, -1):
            
            temp_text2image = Text2Image.from_text(
                text,
                font_size=font_size,
                fill=(105, 61, 36),
                stroke_width=0,
                stroke_fill="white",
            ).wrap(TEXT_MAX_WIDTH)
            
            # 关键修复：先转为Image对象，再获取宽高
            temp_text_img = temp_text2image.to_image()
            temp_width = temp_text_img.width
            temp_height = temp_text_img.height
            
            
            if temp_width <= TEXT_MAX_WIDTH and temp_height <= TEXT_MAX_HEIGHT:
                optimal_font_size = font_size
                break  # 找到最优字号，退出循环

        # 用最优字号生成最终文本图片
        text2image = Text2Image.from_text(
            text,
            font_size=optimal_font_size,
            fill=(105, 61, 36),
            stroke_width=0,
            stroke_fill="white",
        ).wrap(TEXT_MAX_WIDTH)
        text_img = text2image.to_image()

        # 最终校验：即使到最小字号仍超出区域则抛异常
        if text_img.width > TEXT_MAX_WIDTH or text_img.height > TEXT_MAX_HEIGHT:
            raise TextOverLength(
                f"文本过长！即使使用最小字号{min_font_size}，文本尺寸({text_img.width}x{text_img.height})仍超出区域，建议大幅缩短文本"
            )
        # -----------------------------------------------------------------------------------------

        # -------------------------- 调整：8-18帧的y轴坐标全部减5 --------------------------
        # 8-18帧对应的坐标列表（y轴全减5，x轴不变）
        frame_coords = [
            (131, 25),  # 第8帧
            (164, 19),  # 第9帧
            (181, 31),  # 第10帧
            (185, 42),  # 第11帧
            (184, 57),  # 第12帧
            (185, 66),  # 第13帧
            (187, 68),  # 第14帧
            (187, 65),  # 第15帧
            (185, 61),  # 第16帧
            (184, 58),  # 第17帧
            (185, 57),  # 第18帧
        ]

        # 合成帧
        frames = []
        bg_width, bg_height = BuildImage.open(img_dir / "0.png").size  # 提前获取背景尺寸
        for i in range(18):  # 0-17帧（共18帧）
            frame = BuildImage.new("RGBA", (bg_width, bg_height))
            png = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png, (0, 0), alpha=True)

            # 8帧及以后粘贴文本，按索引取对应坐标
            if i >= 7:
                coord_idx = i - 7
                x, y = frame_coords[coord_idx] if coord_idx < len(frame_coords) else frame_coords[-1]
                frame.paste(text_img, (x, y), alpha=True)  # 按修改后坐标粘贴文本

            frames.append(frame.image)

        # 设置帧延迟：最后一帧1秒，其余0.08秒
        durations = [0.08] * len(frames)
        if durations:
            durations[-1] = 1.0

        return save_gif(frames, durations)
    except Exception as e:
        raise e


add_meme(
    "xiaoqiangjupai",
    xiaoqiangjupai,
    min_texts=1,
    max_texts=1,
    default_texts=["活力大湾区，魅力新广州！"],
    keywords=["小强举牌"],
    date_created=datetime(2025, 12, 3),
    date_modified=datetime(2025, 12, 4),  # 修改日期更新为当前日期
)
