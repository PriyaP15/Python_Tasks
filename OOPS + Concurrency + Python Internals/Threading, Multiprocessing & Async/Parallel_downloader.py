import time
import requests
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "DownloadHistory.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

print ("Enter URLs and filenames to download.")
print ("Type 'stop' when you are finished adding files.")

urls=[]
filenames=[]

while True:
    url = input("Enter URL (or 'stop'): ").strip()
    if url.upper() == "STOP":
        break
    
    if not url :
            print ("URL cannot be empty.")
            continue 

    filename =input ("Enter filename to save as: ").strip ()
    if not filename :
        print ("Filename cannot be empty.")
        continue 

    urls.append(url)
    filenames.append(os.path.join(BASE_DIR, filename))


inputs = list(zip(urls, filenames))

def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")

def download_parallel(args):
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap_unordered(download_url, args)
    for result in results:
        if result:
            logging.info(f"url: {result[0]} time (s): {result[1]}")

if __name__ == "__main__":
    t_start = time.time()
    download_parallel(inputs)
    logging.info(f"Downloaded sucessfully within {time.time() - t_start}")
    print('Total parallel time:', time.time() - t_start)