from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def jianpanxia(images: list[BuildImage], texts: list[str], args):
    try:
        if not texts:
            raise ValueError("No text provided")
        text = texts[0]

        text2image = Text2Image.from_text(
            text, 20,fill=(0, 0, 0), stroke_width=0, stroke_fill="white",
        ).wrap(305 - 9)

        # 4. 如果超高就抛异常
        if text2image.height > (171 - 98):
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 2. 合成帧
        frames = []
        bg = BuildImage.open(img_dir / "0.png")
        for i in range(50):
            frame = BuildImage.new("RGBA", (bg.width, bg.height))
            png = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png, (0, 0), alpha=True)

            # 3. 从第41帧开始贴文本（坐标左上角 9,98）
            if i >= 41:
                frame.paste(text_img, (9, 98), alpha=True)

            frames.append(frame.image)

        return save_gif(frames, 0.08)
    except Exception as e:
        raise e

add_meme(
    "jianpanxia",
    jianpanxia,
    min_texts=1,
    max_texts=1,
    default_texts=["来点涩图"],
    keywords=["键盘侠"],
    date_created=datetime(2025, 9, 15),
    date_modified=datetime(2025, 9, 15),
)