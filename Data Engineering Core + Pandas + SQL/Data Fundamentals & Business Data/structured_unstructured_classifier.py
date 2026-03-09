import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "Incoming")
TARGET_BASE = os.path.join(BASE_DIR, "data_files")
structured = os.path.join(TARGET_BASE, "stru_files")
unstructured = os.path.join(TARGET_BASE, "unstru_files")
semistr = os.path.join(TARGET_BASE,"Semi-stru_files")
files_by_extension = {}
summary_data = {}

tasks = []
for file_name in os.listdir(SOURCE_DIR):
    file_path = os.path.join(SOURCE_DIR, file_name) 

    if os.path.isfile(file_path):
        file_extension = os.path.splitext(file_name)[1]

        if file_extension not in files_by_extension:
            files_by_extension[file_extension]=[]

        files_by_extension[file_extension].append(file_path)

for file_extension, file_path in files_by_extension.items():
    folder_name = f"{file_extension[1:].upper()}"

    structured_file_types=["CSV","TSV","XLSX","ODS","SQL","DB","SQLITE"]
    semi_structured_file_types=["JSON","XML","YAML","YML"]

    if folder_name in structured_file_types:
        folder_path = os.path.join(TARGET_BASE,structured)
    elif folder_name in semi_structured_file_types:
        folder_path = os.path.join(TARGET_BASE,semistr)
    else:
        folder_path = os.path.join(TARGET_BASE,unstructured)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for fp in file_path:
        tasks.append((fp, folder_name, folder_path))

    shutil.move(fp, folder_path)