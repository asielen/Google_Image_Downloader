__author__ = 'andrew.sielen'



import time
import urllib
from urllib.request import FancyURLopener
import simplejson
from mimetypes import guess_type, guess_extension



def search_google_images(searchTerm = "",nLinks=10,minWidth=1,minHeight=1,format=""):
    """
        Takes a search term and returns a list of (n_links) urls
    """
    # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = searchTerm.replace(' ','%20')
    searchTerm = searchTerm.replace('\n','')

    if(minWidth is ""): minWidth = 1
    if(minHeight is ""): minHeight = 1
    if(nLinks is ""): nLinks = 10

    nLinks = int(nLinks)

    class MyOpener(FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    myopener = MyOpener()


    imageResults = dict()
    count = 0

    for i in range(0,10):
        if(count>=nLinks): break

        # Notice that the start changes for each iteration in order to request a new set of images for each loop
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+"%20"+format+'&start='+str(i*4)+'&userip=MyIP')
        request = urllib.request.Request(url, None, {'Referer': 'testing'})
        response = urllib.request.urlopen(request)

        # Get results using JSON
        results = simplejson.load(response)
        data = results['responseData']
        if(data is None): continue
        dataInfo = data['results']

        # Iterate for each result and get unescaped url
        for image in dataInfo:
            #if it doesn't meet the dimension requirments
            if(int(image['height']) < int(minHeight) or int(image['width']) < int(minWidth)): continue

            #if it doesn't meet the file format requirements
            if(format is not "" and format not in image['unescapedUrl']): continue

            imageResults[image['title'][:20]] = {"term":searchTerm.replace('%20','_'),"url":image['unescapedUrl'], "height": image['height'], "width":image['width']}
            count += 1
            if(count>=nLinks): break


        # Sleep for one second to prevent IP blocking from Google
        time.sleep(1)

    return imageResults

def download_image(image):
    """
        Takes an image result from the search_google_images function and downloads it
        image is in the format {term,url,height,width}
    """
    class MyOpener(FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    myopener = MyOpener()

    fileExtension = ""

    try:
        fileExtension = guess_extension(guess_type(image['url'])[0])

        myopener.retrieve(image['url'],image['term']+"_"+image['height']+"x"+image['width']+fileExtension)
        print("Downloaded File:  " +image['term']+"_"+image['height']+"x"+image['width']+fileExtension)
    except:
        print("Couldn't get image")