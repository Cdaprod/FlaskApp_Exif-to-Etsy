# generate_metadata.py
import os
import json
import piexif
from PIL import Image

# Function to generate a dictionary containing image metadata
def generate_permanent_dictionary_by_names(directory):
    metadata_dict = {}
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image = Image.open(image_path)
        metadata_dict[filename] = {
            "path": image_path,
            "size": image.size,
            "format": image.format,
            "mode": image.mode,
            "exif": piexif.load(image.info["exif"]),
        }
    return metadata_dict

# Function to generate EXIF data from image names
def generate_permanent_exif_from_names(metadata_dict):
    for filename, image_dict in metadata_dict.items():
        # Here we assume that the filename is in the format of "description.jpg"
        description = filename.replace("_", " ").replace(".jpg", "")
        
        # Generate new EXIF data
        exif_data = image_dict["exif"]
        exif_data["0th"][piexif.ImageIFD.ImageDescription] = description
        image_dict["exif"] = exif_data
    return metadata_dict

# Function to amend generated EXIF data to the metadata dictionary
def amend_generated_exif_to_dictionary(metadata_dict):
    for filename, image_dict in metadata_dict.items():
        exif_data = image_dict["exif"]
        image_dict["exif"] = exif_data
    return metadata_dict

# Function to write metadata dictionary to a JSON file
def write_metadata_to_json(metadata_dict, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(metadata_dict, json_file)

# Usage
directory = "/SRC_IMAGES"
metadata_dict = generate_permanent_dictionary_by_names(directory)
metadata_dict = generate_permanent_exif_from_names(metadata_dict)
metadata_dict = amend_generated_exif_to_dictionary(metadata_dict)
write_metadata_to_json(metadata_dict, "/PATH_TO_JSON/metadata.json")
