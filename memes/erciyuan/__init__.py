from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help_text = "指定名字"


class Model(MemeArgsModel):
    name: str = Field("", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-n", "--name"],
            args=[ParserArg(name="name", value="str")],
            help_text=help_text,
        ),
    ],
)


def erciyuan(images: list[BuildImage], texts: list[str], args: Model):
    # 获取用户头像
    user_img = images[0].convert("RGBA").circle().resize((40, 40))

    # 加载背景图
    background = BuildImage.open(img_dir / "0.png").convert("RGBA")

    # 粘贴头像
    background.paste(user_img, (12, 117), alpha=True)

    # 设置名字默认为“二次元”
    name = args.name or "二次元"

    # 动态字体大小适配
    max_width = 63 - 3
    max_height = 115 - 92
    font_size = 20
    while font_size >= 10:
        name_img = Text2Image.from_text(name, font_size, fill="black").to_image()
        if name_img.width <= max_width and name_img.height <= max_height:
            break
        font_size -= 1
    else:
        font_size = 10  # 最小字体

    name_img = Text2Image.from_text(name, font_size, fill="black").to_image()
    x = 3 + (max_width - name_img.width) // 2
    y = 92 + (max_height - name_img.height) // 2
    background.paste(name_img, (x, y), alpha=True)

    return background.save_jpg()


add_meme(
    "erciyuan",
    erciyuan,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["二次元"],
    date_created=datetime(2025, 9, 5),
    date_modified=datetime(2025, 9, 5),
)
