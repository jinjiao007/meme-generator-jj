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

def myplay(images: list[BuildImage], texts: list[str], args: Model):
    try:
        img = images[0].convert("RGBA").resize((100, 100)).circle()  # 获取用户头像

        # 处理用户名
        name = args.name if args.name else "智商-1"  # 默认用户名
        name_length = len(name)
        font_size = 18
        name_img = Text2Image.from_text(name, font_size, fill="#1b1b1b").to_image()

        # 帧位置定义（从0到15帧的坐标）
        head_locs = [
            (48, 208), (48, 211), (48, 274), (48, 264), (48, 242), (48, 232),
            (48, 221), (48, 209), (48, 208), (48, 272), (48, 245), (48, 240), 
            (48, 225), (48, 216), (48, 208), (48, 205)  
        ]

        # 处理文本
        text = f"{texts[0]}"
        text2image = Text2Image.from_text(text, 35, fill=(0, 0, 0), stroke_width=3, stroke_fill="white", font_families=["033-SSFangTangTi"]).wrap(440)
        if text2image.height > 500:
             raise TextOverLength(texts[0])
        text_img = text2image.to_image()

        # 创建动态帧
        frames = []
        background = BuildImage.open(img_dir / "0.png")  # 打开背景图
        for i in range(16):
            frame = BuildImage.new("RGBA", (background.width, background.height))
            # 粘贴头像
            frame.paste(img, head_locs[i], alpha=True)
            # 粘贴 images 中的 0-15.png
            png_img = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(png_img, alpha=True)
            # 粘贴文本 - 居中对齐
            text_w, _ = text_img.size
            x = (frame.width - text_w) // 2  # 居中对齐的x坐标
            frame.paste(text_img, (x, 265), alpha=True)
            # 粘贴用户名字 - 逐帧移动
            if i < 4:  # 移动10帧后消失
                name_w, name_h = name_img.size
                center_x = name_w // 2
                center_y = name_h // 2
                y = 172 - i * 40  # 逐帧往上移动15个像素
                frame.paste(name_img, (90 - center_x, y - center_y), alpha=True)
            frames.append(frame.image)

        # 返回 GIF 动画
        return save_gif(frames, 0.05)

    except Exception as e:
        print(f"Error generating meme: {e}")
        # 返回一个空的 BytesIO 对象，避免返回 None
        return BytesIO()

def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    """将帧列表保存为GIF动画"""
    buffer = BytesIO()
    # 确保帧数正确
    if not frames:
        return buffer
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
    "myplay",
    myplay,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["笨死了"],
    args_type=args_type,
    keywords=["我敲"],
    date_created=datetime(2025, 5, 17),
    date_modified=datetime(2025, 5, 17),
)
