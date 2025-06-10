from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from PIL.Image import Image as IMG

from meme_generator import add_meme, MemeArgsModel, MemeArgsType, ParserArg, ParserOption
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"
help_text = "指定名字"

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

def qunyoujupai(images: list[BuildImage], texts: list[str], args):
    # 处理用户名
    name = args.name
    if not name:
        name = "晓楠嬢"  # 默认用户名
    if len(name) > 8:
        name = name[:8]  # 限制用户名字数为8个字以内
    name_length = len(name)
    font_size = 72
    name_img = Text2Image.from_text(name, font_size, fill="#1b1b1b").to_image()
    
    img = images[0].convert("RGBA").circle().resize((200, 200))
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:        
        frame.draw_text(
            (136, 385, 494, 546),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=72,
            min_fontsize=18,
            lines_align="center",
            font_families=["FZSJ-QINGCRJ"],
        )
        # 粘贴用户名字
        text_w, _ = name_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(name_img, (x, 26), alpha=True)
        frame.paste(img, (215, 138), alpha=True)        
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "qunyoujupai",
    qunyoujupai,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["我是晓楠嬢"],
    keywords=["群友举牌", "他举牌", "你举牌"],
    args_type=args_type,
    tags=MemeTags.mihoyo,
    date_created=datetime(2025, 6, 10),
    date_modified=datetime(2025, 6, 10),
)
