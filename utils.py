from pil_utils import BuildImage
from meme_generator.utils import split_gif, save_gif


def reduce_frames(img: BuildImage, frame_step: int = 2) -> BuildImage:
  
  """
  对 GIF 动图进行抽帧处理，减少帧数以降低体积。
  - 如果是静态图/动图 < 指定帧数，直接返回原图
  - 如果是动图且帧数 >= GIF_MAX_FRAMES，则按 frame_step 抽帧并保持总时长
  :params
    * ``img``: 输入图片
    * ``frame_step``: 抽帧间隔（默认2表示抽一半）
  """
  max_frame = 60  # 超过这个帧数才触发抽帧
  pil_img = img.image
  if getattr(pil_img, "is_animated", False):
    n_frames = getattr(pil_img, "n_frames", 1)
    if n_frames >= max_frame:
      frames = split_gif(pil_img)
      frames = [
        f.convert("RGBA")
        for i, f in enumerate(frames)
        if i % frame_step == 0
      ]
      duration = pil_img.info.get("duration", 100)
      print(f"[DEBUG] {n_frames} => {len(frames)} 帧, 抽帧完成")
      return BuildImage.open(save_gif(frames, duration * frame_step / 1000))
  # 返回原图
  return img