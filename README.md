# Scrape-Google-Images
Scrape images from Google Images based on search terms given to it. This can be used to generate datasets of images for research or AI.

# Install
```bash
pip3 install scrape-google-images
```
# Example
```py
>>> from scrape_google_images import scrape_google_images
>>> scrape_google_images(download_path="./images/", terms=["dog", "monkey", "elephant"], number_of_images=25, thread_count=3, resolution=[None, None], log=False)
```
```DownloadPath```: The path to an empty directory where the images will be downloaded to.

```Terms```: The search terms that it will use to get the images.

```NumberOfImages```: The number of images for to it will ```try``` scrape for each term.

```ThreadCount```: The amount of threads used to run the program.

```Resolution```: Set the Resolution of the images that will be downloaded. If you do not want to rescale them, put null as shown above. If either Width or Height is set to None, the image will not be rescaled

```log```: Print logs/debugs to see what the program is doing.

# Contributing
If you want to contribute, you can fork this repository and change the code as much as you want. Once you think your code is ready, you can submit a pull request to have the code reviewed by me and hopefully approve your changes.
