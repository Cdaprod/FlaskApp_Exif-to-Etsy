import os
import json
import time
from dotenv import load_dotenv
from pathlib import Path
from ai_image_naming import generate_image_names
from exif_data import apply_exif_data
from etsy_listing import create_etsy_listing

# Load environment variables
load_dotenv()
IMAGES_DIR = os.getenv('IMAGES_DIR')
ETSY_API_KEY = os.getenv('ETSY_API_KEY')
ETSY_SHOP_ID = os.getenv('ETSY_SHOP_ID')

# Load metadata
with open('metadata.json') as f:
    metadata = json.load(f)

# Total number of images
total_images = len(metadata)
processed_images = 0

for image_name, image_data in metadata.items():
    try:
        # Apply exif data
        apply_exif_data(image_name, image_data)

        # Create Etsy listing
        create_etsy_listing(image_name, image_data, ETSY_API_KEY, ETSY_SHOP_ID)

        processed_images += 1
        print(f'Processed {processed_images}/{total_images} images.')

    except Exception as e:
        print(f"An error occurred while processing image {image_name}: {str(e)}")

print("All images processed.")
