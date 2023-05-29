import json
import os
from your_image_processing_module import (
    generate_permanent_names_with_AI,
    generate_permanent_dictonary_by_names,
    generate_permanent_exif_from_names,
    amend_generated_exif_to_dictionary,
    generate_etsy_listing_details_to_dictionary,
)

def run_pipeline(image_folder):
    image_data = {}
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    total_files = len(image_files)

    for i, image_name in enumerate(image_files, 1):
        try:
            print(f"Processing image {i}/{total_files}: {image_name}")

            # Here we're assuming each function returns a new dictionary
            image_data[image_name] = generate_permanent_names_with_AI(image_name, image_data.get(image_name, {}))
            image_data[image_name] = generate_permanent_dictonary_by_names(image_name, image_data.get(image_name, {}))
            image_data[image_name] = generate_permanent_exif_from_names(image_name, image_data.get(image_name, {}))
            image_data[image_name] = amend_generated_exif_to_dictionary(image_name, image_data.get(image_name, {}))
            image_data[image_name] = generate_etsy_listing_details_to_dictionary(image_name, image_data.get(image_name, {}))

            print(f"Successfully processed image {i}/{total_files}: {image_name}")

        except Exception as e:
            print(f"Failed to process image {i}/{total_files}: {image_name}")
            print(f"Error: {str(e)}")

    with open('metadata.json', 'w') as f:
        json.dump(image_data, f)

if __name__ == "__main__":
    run_pipeline('/SRC_IMAGES')
