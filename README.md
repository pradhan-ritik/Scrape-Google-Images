# Scrape-Google-Images
Scrape images from Google Images based on search terms given to it. This can be used to generate datasets of images for research or AI.

# Install
```bash
> git clone git@github.com:flipit001/ScrapeGoogleImages.git
> pip3 install -r requirements.txt
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
    "DownloadPath": "./imgs/",
    "NumberOfImages": 22,
    "ThreadCount": 2,
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
```DownloadPath```: The path where the images will be downloaded to.

```NumberOfImages```: The number of images for to it will ```try``` scrape for each term.

```ThreadCount```: The amount of threads used to run the program.

```Terms```: The search terms that it will use to get the images.