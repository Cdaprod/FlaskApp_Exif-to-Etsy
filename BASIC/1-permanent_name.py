#generate_permanent_names_with_AI.py
import os
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image

# Load the model and feature extractor
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def generate_name(image_path):
    # Open the image file
    try:
        image = Image.open(image_path)
    except IOError:
        print(f'Error: Unable to open {image_path}. Skipping this file.')
        return None

    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    
    # Extract features and generate a description
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    description = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    # Create a new file name based on the description
    # Remove any characters not allowed in file names
    new_name = "".join(c for c in description if c.isalnum() or c.isspace()).rstrip()
    new_name = new_name.replace(" ", "_") + ".jpg"
    return new_name

def rename_files(directory):
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        new_name = generate_name(old_path)

        # If generate_name() returned None, skip this file
        if new_name is None:
            continue

        new_path = os.path.join(directory, new_name)

        # Check if a file with the new name already exists
        if os.path.exists(new_path):
            print(f'Error: File with name {new_name} already exists. Skipping this file.')
            continue

        try:
            os.rename(old_path, new_path)
        except OSError as e:
            print(f'Error: Unable to rename file {old_path} to {new_name}. Reason: {e.strerror}')

# Usage
rename_files('/SRC_IMAGES')
