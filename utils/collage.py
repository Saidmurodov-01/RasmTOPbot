from PIL import Image
import requests
from io import BytesIO

def create_collage(image_urls, output_path="collage.jpg"):
    # Har bir rasmni yuklab, 300x300 ga o‘lchaymiz
    images = [Image.open(BytesIO(requests.get(url).content)).resize((300, 300)) for url in image_urls]
    collage = Image.new("RGB", (900, 600))  # 3 ustun × 2 qator

    for i, img in enumerate(images):
        x = (i % 3) * 300
        y = (i // 3) * 300
        collage.paste(img, (x, y))

    collage.save(output_path)
    return output_path