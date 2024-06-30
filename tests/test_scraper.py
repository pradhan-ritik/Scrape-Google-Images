# path setup 
import sys
sys.path.append("..")
# -------------------

from scrape_google_images import scrape_google_images


if __name__ == "__main__":
    scrape_google_images(download_path="./images/", terms=["dog", "monkey", "elephant"], number_of_images=25, thread_count=3, resolution=[None, None], log=False)
    """
    download_path: The (empty) folder path to where the files will be downloaded to.
    terms: The search terms that will be used by the program to find the images (multi word search terms are allowed).
    number_of_images: The number of images that the program will (try) to scrape from google images.
    thread_count: The number of threads used to scrape the images, 1 by default.
    resolution: The resolution the images will be changed to. If either width of height is none, the changing of resolution will not occur, [None, None] by default.
    log: should the output be printed to the terminal, False by default. For logging it will print 'batches' and how many batches it is done with. One batch is 20 images or one page of google images.
    """