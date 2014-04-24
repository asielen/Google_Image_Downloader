__author__ = 'andrew.sielen'

import imgDownloader
import pprint


def download_logos():

    with open("companies.txt") as f:
        companies = f.readlines()

    for company in companies:
        print("\nGetting Image for "+company)
        image_search_results =  None
        image_search_results = imgDownloader.search_google_images(searchTerm=company+"_logo",nLinks=1,minHeight=100,minWidth=100,format="png")
        for image in image_search_results:
            imgDownloader.download_image(image_search_results[image])

download_logos()

#
# def main():
#
#     pp = pprint.PrettyPrinter(indent=4)
#
#     search_term = input("Search Term: ")
#
#     height = input("Height: ")
#     width = input("Width: ")
#
#     format = input("File Format: ")
#
#     links = input("Number of images: ")
#
#     image_search_results = imgDownloader.search_google_images(search_term,nLinks=links,minHeight=height,minWidth=width,format=format)
#
#     pprint.pprint(image_search_results)
#
#     for image in image_search_results:
#         imgDownloader.download_image(image_search_results[image])
#
#
#
# main()