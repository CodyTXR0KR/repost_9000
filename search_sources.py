# -*- coding: utf-8 -*-

import os
import string
#import requests
import urllib2
import re
#import time

#from urllib2 import urlopen
from cookielib import CookieJar

# Assign headers so google does not think the request is coming from a script
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]


def ImageLookup(path, filename):
    # Google's search by image does not support webm
    # need a check to ensure good results
    print ("")
    print ("Attempting reverse image search on " + path)
    # Also check to see if image was removed
    # path to file on imgur server
    remotepath = 'http://i.imgur.com/' + filename
    # url to perform reverse image search
    googlepath = 'http://www.google.com/searchbyimage?image_url=' + remotepath
    # Visit the url provided
    sourceCode = opener.open(googlepath).read()
    # Remove file extension for URL building (later)
    galleryName = os.path.splitext(filename)[0]
    # Parse output of search (.*? handles any output after regex)
    # Links to pages containing the image
    findLinks = re.findall(r'<div class="rc" data-hveid=".*?">.*?imgurl=(.*?)&amp;', sourceCode)
    # Googles best guess for related keywords (title generation?)
    findBestGuess = re.findall(r'<div class="_hUb">.*?q=(.*?)&amp;', sourceCode)
    # Write results to file for use in description
    print ("")
    print ("Search complete, saving results")
    with open('search_results.txt', 'w') as search_results:
        search_results.write("Search by image URL: " + googlepath + "\n")
        search_results.write("\n")
        if (len(findBestGuess) > 0):
            bestGuess = string.replace(findBestGuess[0], '+', ' ')
            search_results.write("Google best guess: " + bestGuess + "\n")
        search_results.write("Imgur gallery url: http://imgur.com/gallery/" + galleryName + "\n")
        search_results.write("\n")
        search_results.write("Pages containing image:\n")
        for url in findLinks:
            search_results.write(url + "\n")
        search_results.write("\n")

