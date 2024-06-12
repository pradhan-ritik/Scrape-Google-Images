import os.path
import requests
import re
import sys
import urllib.parse
import json
import math
import threading
import PIL.Image
import io


IMG_SEARCH = re.compile(r"\<img\sclass\=\"[^\"]*\"\salt\=\"[^\"]*\"\ssrc\=\"([^\"]*)")

def chunks(terms: list[str], N: int, thread_count: int) -> list[str]:
    sep = math.ceil(N / thread_count)
    for i in range(0, N, sep):
        yield terms[i: i + sep]

def scrape_google_images_threads(thread_count: int, terms: list[str], path: str, num_of_images: int, resolution: tuple[int, int], is_changed_resolution: bool):
    N = len(terms)
    threads = []
    for chunk in chunks(terms, N, thread_count):
        threads.append(threading.Thread(target=scrape_google_images, args=(chunk, path, num_of_images, resolution, is_changed_resolution)))
        
    for i in range(thread_count):
        threads[i].start()

    for i in range(thread_count):
        threads[i].join()

def scrape_google_images(terms: list[str], path: str, num_of_images: int, resolution: tuple[int, int], is_changed_resolution: bool) -> None:
    for term in terms:
        encoded_term = urllib.parse.quote_plus(term)
        folder_path = os.path.join(path, encoded_term)
        os.mkdir(folder_path)

        for i in range(0, num_of_images, 20): # step of 20 because it shows 20 images at a time

            url = f"https://www.google.com/search?q={encoded_term}&udm=2&start={i}"

            page_content = requests.get(url).content.decode(errors="ignore")

            imgs = IMG_SEARCH.findall(page_content)

            if not imgs:
                break

            for idx, img in enumerate(imgs):
                if idx + i >= num_of_images:
                    break
                download_path = os.path.join(folder_path, f"{encoded_term}_{idx+1+i}.jpg") 
                img_to_write = requests.get(img).content
                if is_changed_resolution:
                    PIL.Image.open(io.BytesIO(img_to_write)).resize(resolution).convert('RGB').save(download_path, "JPEG")

                else:
                    PIL.Image.open(io.BytesIO(img_to_write)).convert('RGB').save(download_path, "JPEG")

                print(f"successfully downloaded {download_path}")
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("To use this file, run: python3 scrape_images.py {CONFIG JSON FILE}")

    json_file = sys.argv[1]


    with open(json_file, "r") as fh:
        data = json.load(fh)

    path = data["DownloadPath"]
    terms = data["Terms"]
    num_of_images = data["NumberOfImages"]
    thread_count = data["ThreadCount"]
    resolution = tuple(data["Resolution"])
    is_changed_resolution = resolution[0] and resolution[1]

    if thread_count <= 1:
        scrape_google_images(terms, path, num_of_images, resolution, is_changed_resolution)
    else:
        scrape_google_images_threads(thread_count, terms, path, num_of_images, resolution, is_changed_resolution)