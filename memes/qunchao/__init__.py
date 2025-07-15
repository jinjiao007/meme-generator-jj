from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

def qunchao(images: list[BuildImage], texts, args):    
    background = BuildImage.open(img_dir / "0.png")      
    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((183, 184))
        frame = BuildImage.new("RGBA", background.size, (0, 0, 0, 0))
        frame.paste(img, (197, 198), alpha=True)
        frame.paste(background, (0, 0), alpha=True)        
        return frame
    
    return make_png_or_gif(images, make)

add_meme(
    "qunchao",
    qunchao,
    min_images=1,
    max_images=1,
    keywords=["群嘲", "笑他"],
    date_created=datetime(2025, 7, 15),
    date_modified=datetime(2025, 7, 15),
)