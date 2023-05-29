I see. Here is the updated `README.md`:

---

# Automated Etsy Listing Upload with AI Generated Metadata

This project is designed to automate the process of generating metadata for images and uploading them as listings to an Etsy shop.

## Current Progress

The following steps have been completed:

1. Generation of permanent image names using AI models.
2. Image metadata generation, including creation of a `metadata.json` file.

## Files

- `generate_permanent_names_with_AI.py`: This script uses AI models to generate permanent image names.
- `generate_metadata.py`: This script generates image metadata, including EXIF data from image names, and writes this metadata to a `metadata.json` file.

## Todo

1. **Automated Etsy Listing Upload:** Write a script to automatically upload the processed images as listings to an Etsy shop. This script should read from the `metadata.json` file to get the required metadata for each image.

## How to Proceed

- Images should be already edited and placed in the `/SRC_IMAGES` directory.
- Run `generate_permanent_names_with_AI.py` to generate AI-based names for your images.
- Run `generate_metadata.py` to generate metadata for your images and write it to a `metadata.json` file.
- Write and run a script to upload your images as listings to an Etsy shop using the Etsy API and the metadata from `metadata.json`.