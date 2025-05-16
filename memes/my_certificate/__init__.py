from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def my_certificate(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA")  # 获取用户头像

    # 将头像处理为150x150的圆形
    img_circle = img.resize((150, 150)).circle()
    # 将头像处理为31x33的方形
    img_square = img.resize((31, 33))

    # 打开背景图niuma.png
    background = BuildImage.open(img_dir / "niuma.png")

    # 粘贴圆形头像到(94,60)
    background.paste(img_circle, (94, 60), alpha=True)
    # 粘贴方形头像到(258,207)
    background.paste(img_square, (258, 207), alpha=True)

    # 处理文本
    if texts:
        text = f"这是我的{texts[0]}证"
        text2image = Text2Image.from_text(text, 40, fill="white", stroke_fill="black").wrap(440)
        if text2image.height > 500:
            raise TextOverLength(text)
        text_img = text2image.to_image()

        # 创建一个新的空白画布
        new_background = BuildImage.new("RGBA", (background.width, background.height))
        # 粘贴背景图到新画布
        new_background.paste(background)
        # 粘贴文本图到新画布的指定位置，例如(20, 268)
        new_background.paste(text_img, (20, 268), alpha=True)

        # 将最终的图片保存为字节流
        buffer = BytesIO()
        new_background.image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    else:
        # 如果没有提供文本，直接返回背景图
        buffer = BytesIO()
        background.image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer


add_meme(
    "my_certificate",
    my_certificate,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["牛马"],
    keywords=["我的证"],
    date_created=datetime(2025, 5, 14),
    date_modified=datetime(2025, 5, 14),
)