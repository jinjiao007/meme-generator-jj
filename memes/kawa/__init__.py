from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def kawa(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        # 先绘制白色描边（8个方向偏移）
        for dx, dy in [(-2,-2), (-2,0), (-2,2), (0,-2), (0,2), (2,-2), (2,0), (2,2)]:
            frame.draw_text(
                (70+dx, 120+dy, 412+dx, 231+dy),  # 添加偏移量
                text,
                fill=(0, 0, 0),  # 白色描边
                allow_wrap=True,
                max_fontsize=255,
                min_fontsize=20,
                lines_align="center",
                font_families=["033-SSFangTangTi"],
            )

            # 再绘制原始粉色文字
            frame.draw_text(
            (70, 120, 412, 231),
            text,
            fill=(255, 180, 221),  # 原始粉色
            allow_wrap=True,
            max_fontsize=250,
            min_fontsize=20,
            lines_align="center",
            font_families=["033-SSFangTangTi"],
            )
   
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "kawa",
    kawa,
    min_texts=1,
    max_texts=1,
    default_texts=["卡哇伊"],
    keywords=["kawa", "卡哇伊"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 7, 8),
    date_modified=datetime(2025, 7, 8),
)
