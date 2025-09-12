from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from PIL.Image import Image as IMG

from meme_generator import add_meme, MemeArgsModel, MemeArgsType, ParserArg, ParserOption
from meme_generator.exception import TextOverLength


img_dir = Path(__file__).parent / "images"
help_text = "指定文本"

# 添加 Model 类，用于处理命令行参数
class Model(MemeArgsModel):
    name: str = ""

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

def goujiao(images: list[BuildImage], texts: list[str], args: Model):
    # 1. 处理用户名
    name = args.name or "不服你也爆"      # 缺省值
    name = name[:10]                      # 超长截断

    # 2. 准备素材
    img = images[0].convert("RGBA").circle().resize((78, 78))
    text = texts[0]
    frame_bg = BuildImage.open(img_dir / "0.png")
    frame = BuildImage.new("RGBA", frame_bg.size, (0, 0, 0, 0))

    try:
        # 3. 贴底图 & 头像
        frame.paste(frame_bg, (0, 0), alpha=True)
        frame.paste(img, (300, 151), alpha=True)

        # 4. 画文字（主文案）
        frame.draw_text(
            (298, 136, 376, 150),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=25,
            min_fontsize=10,
            lines_align="center",
        )

        # 5. 画用户名（指定区域 + 字号 10~18 + 居中）
        frame.draw_text(
            (403, 115, 477, 170),
            name,
            fill=(0, 0, 0),
            max_fontsize=18,
            min_fontsize=10,
            halign="center",
            valign="center",
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_jpg()


add_meme(
    "goujiao",
    goujiao,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["下头豹"],
    keywords=["狗叫"],
    args_type=args_type,
    date_created=datetime(2025, 9, 12),
    date_modified=datetime(2025, 9, 12),
)
