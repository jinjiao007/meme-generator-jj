from datetime import datetime
from pathlib import Path
import math

import dateparser
from pil_utils import BuildImage
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

class Model(MemeArgsModel):
    time: str = Field("", description="指定时间")

args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-t", "--time"],
            args=[ParserArg(name="time", value="str")],
            help_text="指定时间",
        ),
    ],
)


def downban(images: list[BuildImage], texts: list[str], args: Model):
    time = datetime.now()
    if args.time and (parsed_time := dateparser.parse(args.time)):
        time = parsed_time

    img = images[0].convert("RGBA").circle().resize((80, 80))
    frame = BuildImage.open(img_dir / "0.png").convert("RGBA")

    # 创建时间文本图像
    time_text = f"[u]{time.hour}[/u]时[u]{time.minute}[/u]分[u]{time.second}[/u]秒"
    
    # 创建临时画布绘制时间文本
    temp_img = BuildImage.new("RGBA", (300, 50), (0, 0, 0, 0))
    temp_img.draw_bbcode_text(
        (0, 0, temp_img.width, temp_img.height),
        text=time_text,
        max_fontsize=40,
        min_fontsize=20,
        fill=(255, 255, 255),
        halign="center",
        valign="center"
    )
    
    # 旋转时间文本图像 (逆时针22°)
    rotated_text = temp_img.image.rotate(
        22,  # 逆时针旋转角度
        expand=True,  # 扩展画布以适应旋转后的图像
        fillcolor=(0, 0, 0, 0)  # 透明背景
    )
    
    # 计算粘贴位置 (目标位置是旋转后图像的中点)
    target_x, target_y = 237, 298  # 目标位置
    
    # 计算旋转后图像的尺寸
    rotated_width, rotated_height = rotated_text.size
    
    # 计算粘贴位置 (使旋转后图像的中心点位于目标位置)
    paste_x = target_x - rotated_width // 2
    paste_y = target_y - rotated_height // 2
    
    # 将旋转后的时间文本粘贴到主图像上
    frame.image.paste(rotated_text, (int(paste_x), int(paste_y)), rotated_text)
    
    # 粘贴用户头像
    frame.paste(img, (208, 76), alpha=True)
    return frame.save_jpg()


add_meme(
    "downban",
    downban,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    args_type=args_type,
    keywords=["下班"],
    date_created=datetime(2025, 6, 13),
    date_modified=datetime(2025, 6, 14),
)