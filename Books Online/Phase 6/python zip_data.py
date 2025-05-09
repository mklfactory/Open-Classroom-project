import zipfile
import os

# Définir le chemin du dossier à compresser et le nom de l'archive
base_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(base_dir, 'data')
output_zip = os.path.join(base_dir, 'data_export.zip')

# Créer une archive ZIP contenant tout le dossier data
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, data_folder)
            zipf.write(file_path, arcname)

print(f'✅ Archive créée avec succès : {output_zip}')
