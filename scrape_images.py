import os.path
import requests
import re
import sys
import urllib.parse
import json

IMG_SEARCH = re.compile(r"\<img\sclass\=\"[^\"]*\"\salt\=\"[^\"]*\"\ssrc\=\"([^\"]*)")

def scrape_google_images(terms: list[str], path: str):
    for term in terms:

        encoded_term = urllib.parse.quote_plus(term)

        folder_path = os.path.join(path, encoded_term)
        os.mkdir(folder_path)

        url = f"https://www.google.com/search?q={encoded_term}&udm=2"

        page_content = requests.get(url).content.decode()

        imgs = IMG_SEARCH.findall(page_content)

        for idx, img in enumerate(imgs):
            img_to_write = requests.get(img)
            download_path = os.path.join(folder_path, f"{encoded_term}_{idx+1}.jpg") 
            with open(download_path, "wb") as fh:
                fh.write(img_to_write.content)
            print(f"successfully downloaded {download_path}")
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("To use this file, run: python3 scrape_images.py {JSON FILE} {DOWNLOAD_PATH}")

    json_file = sys.argv[1]
    path = sys.argv[2]


    with open(json_file, "r") as fh:
        terms = json.load(fh)

    scrape_google_images(terms, path)