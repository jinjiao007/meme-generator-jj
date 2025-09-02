from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

# 导入工具包
import importlib.util
util_dir = Path(__file__).parents[2] / "utils.py"
spec = importlib.util.spec_from_file_location("utils", util_dir)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

img_dir = Path(__file__).parent / "images"

default_text = "收款码"

def payment_code(images: list[BuildImage], texts: list[str], args):
    # gif检测
    images = [utils.reduce_frames(img) for img in images]

    frame = BuildImage.open(img_dir / "0.png").convert("RGBA")
    text = texts[0] if texts else default_text
    try:
        frame.draw_text(
            (60, frame.height - 120, frame.width - 70, frame.height - 10),
            text,
            min_fontsize=30,
            max_fontsize=60,
            fill="white",
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((360, 360), keep_ratio=True, inside=True)
        return frame.copy().paste(img, (120, 220), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "payment_code",
    payment_code,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["收款码", "付款码"],
    date_created=datetime(2024, 5, 12),
    date_modified=datetime(2024, 5, 16),
)
