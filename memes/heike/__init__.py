from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "嘿客"

def heike(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    text2image = Text2Image.from_text(
        text, 40, fill=(255, 255, 255), stroke_width=1, stroke_fill="black",
        font_families=["GlowSansSC-Normal-Heavy"]
    ).wrap(200)
    if text2image.height > 80:
        raise TextOverLength(text)
    text_img = text2image.to_image()
    
    background = BuildImage.open(img_dir / "0.png")  
    
    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((200, 200))
        frame = BuildImage.new("RGBA", background.size, (0, 0, 0, 0))
        frame.paste(img, (75, 17), alpha=True)
        frame.paste(background, (0, 0), alpha=True)
        x = (background.width - text_img.width) // 2
        y = 215 
        frame.paste(text_img, (x, y), alpha=True)
        
        return frame
    
    return make_png_or_gif(images, make)

add_meme(
    "heike",
    heike,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["嘿壳", "黑客", "嘿客"],
    date_created=datetime(2025, 6, 27),
    date_modified=datetime(2025, 6, 27),
)