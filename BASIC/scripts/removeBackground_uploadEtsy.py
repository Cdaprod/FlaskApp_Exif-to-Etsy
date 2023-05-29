from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

ETSY_API_KEY = os.getenv("ETSY_API_KEY")
ETSY_OAUTH_TOKEN = os.getenv("ETSY_OAUTH_TOKEN")

def remove_background(input_image_path):
    img = Image.open(input_image_path)
    img = img.convert("RGBA")

    datas = img.getdata()

    new_data = []
    for item in datas:
        # change all white (also shades of whites)
        # pixels to transparent
        if item[0] in list(range(200, 256)):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

def upload_image_to_etsy(image, listing_id):
    url = f"https://api.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}/images"
    headers = {
        "Content-Type": "image/png",
        "x-api-key": ETSY_API_KEY,
        "Authorization": f"Bearer {ETSY_OAUTH_TOKEN}"
    }
    response = requests.post(url, headers=headers, data=image)
    return response.json()

def main():
    input_image_path = "path_to_your_image.png"
    listing_id = "your_listing_id"
    img = remove_background(input_image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = buffered.getvalue()
    response = upload_image_to_etsy(img_str, listing_id)
    print(response)

if __name__ == "__main__":
    main()
