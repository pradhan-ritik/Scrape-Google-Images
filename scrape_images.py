import urllib.parse
import requests
import re
import sys
import os.path

if len(sys.argv) < 3:
    raise Exception("To use this file, run: python3 scrape_images.py {TERM} {DOWNLOAD_PATH}")

term = sys.argv[1]
path = sys.argv[2]

IMG_SEARCH = re.compile(r"\<img\sclass\=\"[^\"]*\"\salt\=\"[^\"]*\"\ssrc\=\"([^\"]*)")


encoded_term = urllib.parse.quote_plus(term)

url = f"https://www.google.com/search?q={encoded_term}&udm=2"

page_content = requests.get(url).content.decode()

imgs = IMG_SEARCH.findall(page_content)

for idx, img in enumerate(imgs):
    img_to_write = requests.get(img)
    with open(os.path.join(path, f"{encoded_term}_{idx+1}.jpg"), "wb") as fh:
        fh.write(img_to_write.content)
    print(f"successfully downloaded {encoded_term}_{idx+1}.jpg")