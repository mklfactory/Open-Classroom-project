import zipfile
import os

# Define the path to the folder to be compressed and the name of the archive
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
data_folder = os.path.join(base_dir, 'data')  # Path to the 'data' folder
output_zip = os.path.join(base_dir, 'data_export.zip')  # Name and path of the ZIP archive to be created

# Create a ZIP archive containing the entire 'data' folder
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Walk through the 'data' folder and its subfolders
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            file_path = os.path.join(root, file)  # Full path to the file
            arcname = os.path.relpath(file_path, data_folder)  # Relative path of the file within the 'data' folder
            zipf.write(file_path, arcname)  # Add the file to the ZIP archive

# Print success message with the location of the created ZIP archive
print(f'✅ Archive created successfully: {output_zip}')