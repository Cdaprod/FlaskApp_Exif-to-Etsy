from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import requests
import torch
from PIL import Image

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def get_image_title(image_path):
    # Open the image and convert to RGB if necessary
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
        i_image = i_image.convert(mode="RGB")

    # Prepare the image
    pixel_values = feature_extractor(images=i_image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Generate image description
    output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
    title = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return title

def create_listing(image_path, who_made, price, made_when, taxonomy_id, image_ids, api_key, oauth_token, shop_id):
    # Generate a descriptive title for the image
    title = get_image_title(image_path)

    # Set headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"Bearer {oauth_token}"
    }

    # Build request body
    body = {
        "quantity": 1,
        "title": title,
        "description": title,
        "price": price,
        "who_made": who_made,
        "when_made": made_when,
        "taxonomy_id": taxonomy_id,
        "image_ids": image_ids,
        "is_digital": True
    }

    # Make POST request to create the draft listing
    response = requests.post(
        f"https://api.etsy.com/v3/application/shops/{shop_id}/listings",
        headers=headers,
        data=body
    )

    # Check the response
    if response.status_code == 201:
        print("Listing created successfully!")
    else:
        print(f"Failed to create listing: {response.content}")

# Replace with your actual values
image_path = 'doctor.e16ba4e4.jpg'
who_made = "CDA Photography"
price = "1000"
made_when = "2023-05-29"
taxonomy_id = "1"
image_ids = "378848,238298,030076"
api_key = "your_api_key"
oauth_token = "your_oauth_token"
shop_id = "12345678"

create_listing(image_path, who_made, price, made_when, taxonomy_id, image_ids, api_key, oauth_token, shop_id)
