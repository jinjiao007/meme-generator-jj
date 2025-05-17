from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from io import BytesIO
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsModel, MemeArgsType, ParserArg, ParserOption

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

def gongzei(images: list[BuildImage], texts: list[str], args: Model):
    img = images[0].convert("RGBA").resize((164, 164)).circle()  # 获取用户头像

    # 处理用户名
    name = args.name
    if not name:
        name = "工贼"  # 默认用户名
    if len(name) > 8:
        name = name[:8]  # 限制用户名字数为8个字以内
    name_length = len(name)
    font_size = 18
    name_img = Text2Image.from_text(name, font_size, fill="#1b1b1b").to_image()

    # 将文本图片逆时针旋转7°
    name_img = name_img.rotate(7, expand=True)

    # 帧位置定义（从0到3帧的坐标）
    head_locs = [(64, 60), (54, 55), (41, 55), (55, 59)]
    name_locs = [(225, 242), (225, 240), (225, 242), (225, 240)]

    # 处理文本
    text = f"{texts[0]}"
    text2image = Text2Image.from_text(text, 42, fill="black", font_families=["033-SSFangTangTi"]).wrap(440)
    if text2image.height > 500:
         raise TextOverLength(texts[0])
    text_img = text2image.to_image()

    # 创建动态帧
    frames = []
    background = BuildImage.open(img_dir / "dengzi.png")  # 打开背景图
    for i in range(4):
        frame = BuildImage.new("RGBA", (background.width, background.height))
        frame.paste(background)
        # 粘贴头像
        frame.paste(img, head_locs[i], alpha=True)
        # 粘贴 images 中的 0-3.png
        png_img = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(png_img, alpha=True)
        # 粘贴文本 - 居中对齐
        text_w, _ = text_img.size
        x = (frame.width - text_w) // 2  # 居中对齐的x坐标
        frame.paste(text_img, (x, 258), alpha=True)
        # 粘贴用户名字
        name_w, name_h = name_img.size
        center_x = name_w // 2
        center_y = name_h // 2
        frame.paste(name_img, (name_locs[i][0] - center_x, name_locs[i][1] - center_y), alpha=True)
        frames.append(frame.image)

    # 返回 GIF 动画
    return save_gif(frames, 0.08)

def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=int(duration * 1000),
        loop=0,
        disposal=2  # 确保每一帧在显示下一帧前会被正确清除
    )
    buffer.seek(0)
    return buffer

add_meme(
    "gongzei",
    gongzei,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["我爱加班"],
    args_type=args_type,
    keywords=["工贼"],
    date_created=datetime(2025, 5, 17),
    date_modified=datetime(2025, 5, 17),
)