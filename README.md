# Scrape-Google-Images
Scrape images from Google Images based on a term. This can be used to generate datasets of images for research or AI. It will get exactly 20 images per term.

# Download
```bash
> git clone git@github.com:flipit001/ScrapeGoogleImages.git
```
# Use
```bash
> python3 scrape_images.py {CONFIG JSON FILE}
```
## Example
```bash
> mkdir images # make sure this directory is empty
> cat example.json
{
    "DownloadPath": "./images/",
    "ThreadCount": 1,
    "Terms": [
        "Dog",
        "Elephant",
        "Badger",
        "Bear",
        "Falcon",
        "Tiger"
    ]
}
> python3 scrape_images.py example.json
```
