from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

def sayguaihua(images, texts: list[str], args):
    text = f"{texts[0]}"
    text2image = Text2Image.from_text(
        text, 25, fill=(0, 0, 0), stroke_width=1, stroke_fill="white",        
    ).wrap(590)
    if text2image.height > 80:
        raise TextOverLength(text)
    text_img = text2image.to_image()

    fg = BuildImage.open(img_dir / "0.png")
    w_fg, h = fg.size

    # 1. 底图比前景宽 400px
    extra_width = 400
    base = BuildImage.new("RGBA", (w_fg + extra_width, h), "#efe8d5")

    frames = []
    for i in range(30):
        frame = base.copy()
        # 文字从右侧外进入，每帧左移 15 px
        x = base.width - i * 15
        frame.paste(text_img, (x, 33), alpha=True)
        # 把前景盖在最上面（前景靠右对齐，保持视觉位置）
        frame.paste(fg, (extra_width, 0), alpha=True)
        frames.append(frame.image)

    # 输出尺寸统一为前景大小（裁剪掉左侧多余部分）
    frames = [f.crop((extra_width, 0, extra_width + w_fg, h)) for f in frames]

    return save_gif(frames, 0.05)


add_meme(
    "sayguaihua",
    sayguaihua,
    min_texts=1,
    max_texts=1,
    default_texts=["你好会上班哦~"],
    keywords=["说怪话", "阴阳大师"],
    tags=MemeTags.bronya,
    date_created=datetime(2025, 9, 29),
    date_modified=datetime(2025, 9, 29),
)