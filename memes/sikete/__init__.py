from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from PIL.Image import Image as IMG

from meme_generator import add_meme, MemeArgsModel, MemeArgsType, ParserArg, ParserOption
from meme_generator.exception import TextOverLength


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

def sikete(images: list[BuildImage], texts: list[str], args: Model):
    # 处理用户名
    name = args.name
    if not name:
        name = "正义斯科特"  # 默认用户名
    if len(name) > 20:
        name = name[:20]  # 限制用户名字数为20个字以内
    name_length = len(name)
    font_size = 18
    name_img = Text2Image.from_text(name, font_size, fill="#e8d6ad").to_image()
    
    img = images[0].convert("RGBA").circle().resize((260, 230))
    text = texts[0]
    frame_bg = BuildImage.open(img_dir / "0.png")  # 背景图片
    frame = BuildImage.new("RGBA", frame_bg.size, (0, 0, 0, 0))
    
    try:
        frame.paste(img, (135, 31), alpha=True)
        frame.paste(frame_bg, (0, 0), alpha=True)
        
        # 绘制文本和名字（在背景上层）
        frame.draw_text(
            (136, 382, 360, 437),
            text,
            fill=(255, 255, 255),
            allow_wrap=True,
            max_fontsize=18,
            min_fontsize=18,
            lines_align="center",
            #font_families=["FZSJ-QINGCRJ"],
        )
        # 粘贴用户名字
        text_w, _ = name_img.size
        x = (frame.width - text_w) // 2 - 80 # 居中对齐的x坐标
        frame.paste(name_img, (x, 348), alpha=True)
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "sikete",
    sikete,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["那我的屁股怎么办"],
    keywords=["斯科特"],
    args_type=args_type,
    date_created=datetime(2025, 7, 13),
    date_modified=datetime(2025, 7, 13),
)
