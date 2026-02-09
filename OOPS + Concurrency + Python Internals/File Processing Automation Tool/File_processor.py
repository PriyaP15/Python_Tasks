import os
import shutil
import logging
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = r"C:\Users\priya\Desktop\generated\Incoming"
TARGET_BASE = os.path.join(BASE_DIR, "processed_data")
SUMMARY_FILE = os.path.join(BASE_DIR, "summary.json")
LOG_FILE = os.path.join(BASE_DIR,"automation.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

files_by_extension = {}
summary_data = {}

def data_eval(df,fn):
    logging.info(f"Processing started for {fn}")

    req_cols = ['Product', 'Quantity', 'Amount']
    
    cols_pres = True
    for col in req_cols:
        if col not in df.columns:
            cols_pres = False
    
    if cols_pres:
        product_group = df.groupby('Product')[['Quantity', 'Amount']].sum()
        product_dtls = product_group.to_dict(orient='index')
        total = round(float(df['Amount'].sum()),2)

        summary_data[fn] = {"total sales": round(total,2),"products": product_dtls}
        
        logging.info(f"Processing finished for {fn}")
    else:
        logging.warning(f"Skipping {fn}: Missing required columns {req_cols}")

def processing(file_info):
    fp, folder_name, folder_path = file_info
    try:
        fn = os.path.basename(fp)
        destf = os.path.basename(folder_path)
        fd = os.path.join(folder_path, fn)
        shutil.move(fp, folder_path)
        logging.info(f"Moved {fn} to {destf}")

        if folder_name == "CSV":
            df = pd.read_csv(fd)
            data_eval(df,fn)

        elif folder_name == "XLSX":
            df = pd.read_excel(fd)
            data_eval(df,fn)
            

    except Exception as e:
        logging.error(f"Failed to move {fp}: {e}")

            
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
    if folder_name == "CSV":
        folder_path = os.path.join(TARGET_BASE,"Sales reports")
    elif folder_name == "JSON":
        folder_path = os.path.join(TARGET_BASE,"User activity logs")
    elif folder_name == "TXT":
        folder_path = os.path.join(TARGET_BASE,"Server error dumps")
    elif folder_name == "XLSX":
        folder_path = os.path.join(TARGET_BASE,"Excel files")
    else:
        folder_path = os.path.join(TARGET_BASE,"Others")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for fp in file_path:
        tasks.append((fp, folder_name, folder_path))

max_workers = os.cpu_count() or 1
if tasks:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(processing, tasks)

if summary_data:
    with open(SUMMARY_FILE, 'w') as f:
        json.dump(summary_data, f, indent=4)
    logging.info(f"Summary saved to {os.path.basename(SUMMARY_FILE)}")
