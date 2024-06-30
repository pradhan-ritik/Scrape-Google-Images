import os.path
import requests
import re
import urllib.parse
import math
import PIL.Image
import io
import multiprocessing

__all__ = [
    "scrape_google_images"
]

_IMG_SEARCH = re.compile(r"\<img\sclass\=\"[^\"]*\"\salt\=\"[^\"]*\"\ssrc\=\"([^\"]*)")

def _chunks(terms: list[str], N: int, thread_count: int) -> list[str]:
    sep = math.ceil(N / thread_count)
    for i in range(0, N, sep):
        yield terms[i: i + sep]

def _scrape_google_images_threads(thread_count: int, terms: list[str], path: str, num_of_images: int, resolution: tuple[int, int], is_changed_resolution: bool, log: bool):
    N = len(terms)
    threads = []
    for chunk in _chunks(terms, N, thread_count):
        threads.append(multiprocessing.Process(target=_scrape_google_images, args=(chunk, path, num_of_images, resolution, is_changed_resolution, log)))
        
    for i in range(thread_count):
        threads[i].start()

    for i in range(thread_count):
        threads[i].join()

def _scrape_google_images(terms: list[str], path: str, num_of_images: int, resolution: tuple[int, int], is_changed_resolution: bool, log: bool) -> None:
    for term in terms:
        encoded_term = urllib.parse.quote_plus(term)
        folder_path = os.path.join(path, encoded_term)
        os.mkdir(folder_path)

        for i in range(0, num_of_images, 20): # step of 20 because it shows 20 images at a time

            url = f"https://www.google.com/search?q={encoded_term}&udm=2&start={i}"

            page_content = requests.get(url).content.decode(errors="ignore")

            imgs = _IMG_SEARCH.findall(page_content)

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

            if log:
                print(f"finished with batch {int(i/20)+1} for {term}")

def scrape_google_images(download_path: str, terms: str, number_of_images: int, thread_count: int = 1, resolution: tuple[int | None] = tuple([None, None]), log: bool = False) -> None:
    is_changed_resolution = resolution[0] and resolution[1]
    if thread_count <= 1:
        _scrape_google_images(terms, download_path, number_of_images, resolution, is_changed_resolution, log)
    else:
        _scrape_google_images_threads(thread_count, terms, download_path  , number_of_images, resolution, is_changed_resolution, log)