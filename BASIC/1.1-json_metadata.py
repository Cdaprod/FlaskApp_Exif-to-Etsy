import json
import os

# Load the JSON file (or create a new one if it doesn't exist)
if os.path.exists('file_data.json'):
    with open('file_data.json', 'r') as f:
        file_data = json.load(f)
else:
    file_data = {}

# Process files
for filename in os.listdir('my_folder'):
    if filename not in file_data or file_data[filename]['status'] != 'processed':
        # Process the file here
        # ...

        # Update file_data with the new information
        file_data[filename] = {
            'status': 'processed',
            'new_name': 'new_name',
            'description': 'description',
            # ...
        }

# Save file_data back to the JSON file
with open('file_data.json', 'w') as f:
    json.dump(file_data, f)
