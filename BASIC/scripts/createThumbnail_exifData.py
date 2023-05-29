import os
import json
import datetime
from PIL import Image
import piexif

def generate_exif_data(directory, creator, date):
    data_dict = {}

    for filename in os.listdir(directory):
        # Skip non-image files
        if not filename.endswith(".jpg"):
            continue

        image_path = os.path.join(directory, filename)

        # Create the EXIF data
        exif_dict = {
            "0th": {
                piexif.ImageIFD.Artist: creator,
                piexif.ImageIFD.DateTime: date,
            },
            "Exif": {},
            "GPS": {},
            "1st": {},
            "thumbnail": None,
        }

        # Extract the filename without extension to use as title and description
        name = os.path.splitext(filename)[0]
        description = name.replace("_", " ").capitalize()

        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description
        exif_dict["0th"][piexif.ImageIFD.DocumentName] = name

        # Open the image and create a thumbnail
        with Image.open(image_path) as img:
            thumbnail_size = (200, 200)  # Adjust to the desired thumbnail size
            img.thumbnail(thumbnail_size)

            # Convert the thumbnail image to bytes and include it in the EXIF data
            thumbnail_bytes = io.BytesIO()
            img.save(thumbnail_bytes, format='JPEG')
            exif_dict["thumbnail"] = thumbnail_bytes.getvalue()

            # Convert the EXIF data to bytes and save the image with the EXIF data
            exif_bytes = piexif.dump(exif_dict)
            img.save(image_path, exif=exif_bytes)

        # Add the generated EXIF data to the dictionary
        data_dict[filename] = exif_dict

    # Write the dictionary to a JSON file
    with open('metadata.json', 'w') as f:
        json.dump(data_dict, f)

# Usage
generate_exif_data('/path/to/your/directory', 'CDA Photography', datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S"))
