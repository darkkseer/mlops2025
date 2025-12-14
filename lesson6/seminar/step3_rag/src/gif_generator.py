import base64
import io
from PIL import Image

def base64_to_image(b64: str) -> Image.Image:
    img_data = base64.b64decode(b64)
    return Image.open(io.BytesIO(img_data))

def create_gif(images: list, output_path: str, duration: int = 500):
    """Создаёт GIF из списка PIL.Image"""
    if not images:
        raise ValueError("No images to create GIF")
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )