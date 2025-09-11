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


def zhiyexuanshou(images: list[BuildImage], texts: list[str], args: Model):
    # 获取用户头像
    user_img = images[0].convert("RGBA").circle().resize((50, 50))

    # 加载背景图
    background = BuildImage.open(img_dir / "0.png").convert("RGBA")

    # 粘贴头像
    background.paste(user_img, (64, 3), alpha=True)

        # 设置名字默认为“某某职业选手”
    name = args.name or "某某职业选手"

    # 竖排文字绘制区域
    x0, y0 = 162, 14          # 左上角
    x1, y1 = 214, 275         # 右下角
    box_w = x1 - x0           # 可用宽度
    box_h = y1 - y0           # 可用高度

    # 从大到小试字号
    font_size = 20
    while font_size >= 10:
        # 每个字单独成像，竖排
        char_imgs = [Text2Image.from_text(ch, font_size, fill="black").to_image()
                     for ch in name]
        char_w = max(im.width for im in char_imgs)
        total_h = sum(im.height for im in char_imgs)
        if char_w <= box_w and total_h <= box_h:
            break
        font_size -= 1
    else:
        font_size = 10          # 强制最小
        char_imgs = [Text2Image.from_text(ch, font_size, fill="black").to_image()
                     for ch in name]

    # 竖排拼接
    char_w = max(im.width for im in char_imgs)
    total_h = sum(im.height for im in char_imgs)
    vertical = BuildImage.new("RGBA", (char_w, total_h), (0, 0, 0, 0))
    y_cursor = 0
    for im in char_imgs:
        dx = (char_w - im.width) // 2
        vertical.paste(im, (dx, y_cursor), alpha=True)
        y_cursor += im.height

    # 居中对齐到目标矩形
    x = x0 + (box_w - char_w) // 2
    y = y0 + (box_h - total_h) // 2
    background.paste(vertical, (x, y), alpha=True)

    return background.save_jpg()


add_meme(
    "zhiyexuanshou",
    zhiyexuanshou,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["职业选手"],
    date_created=datetime(2025, 9, 11),
    date_modified=datetime(2025, 9, 11),
)
