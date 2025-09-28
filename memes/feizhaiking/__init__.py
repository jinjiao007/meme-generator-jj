from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

def feizhaiking(images: list[BuildImage], texts: list[str], args):
    text = f"{texts[0]}"
    text2image = Text2Image.from_text(
        text, 40, fill=(0, 0, 0), stroke_width=1, stroke_fill="white",        
    ).wrap(590)
    if text2image.height > 80:
        raise TextOverLength(text)
    text_img = text2image.to_image()
    
    background = BuildImage.open(img_dir / "0.png")  
    
    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((271, 233))
        frame = BuildImage.new("RGBA", background.size, (0, 0, 0, 0))
        frame.paste(img, (126, 151), alpha=True)
        frame.paste(background, (0, 0), alpha=True)
        x = (background.width - text_img.width) // 2
        y = 498 
        frame.paste(text_img, (x, y), alpha=True)
        
        return frame
    
    return make_png_or_gif(images, make)

add_meme(
    "feizhaiking",
    feizhaiking,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["肥猪网络皇帝"],
    keywords=["肥仔网络皇帝", "网络皇帝", "皇帝"],
    date_created=datetime(2025, 6, 27),
    date_modified=datetime(2025, 6, 27),
)