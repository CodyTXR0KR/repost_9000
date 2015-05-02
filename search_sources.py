# -*- coding: utf-8 -*-

import os
import string
import requests
import urllib2
import json
import re
import time

from urllib2 import urlopen
from cookielib import CookieJar
from helpers import get_config

# Assign headers so google does not think the request is coming from a script
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]


def GoogleLookup(filename):
    # Clear old search results
    #os.remove('search_results.txt')
    # Remove file extension for URL building (later)
    galleryName = os.path.splitext(filename)[0]

    if (filename.endswith('webm')):
        with open('search_results.txt', 'w') as search_results:
            search_results.write("Google Reverse image lookup does not support this file format \n" + "\n")
            search_results.write("Where I found it: http://imgur.com/gallery/" + galleryName + "\n")
    else:
        print ("")
        print ("Attempting reverse image search")
        # Also check to see if image was removed
        # path to file on imgur server
        remotepath = 'http://i.imgur.com/' + filename
        # url to perform reverse image search
        googlepath = 'http://www.google.com/searchbyimage?image_url=' + remotepath
        # Visit the url provided
        sourceCode = opener.open(googlepath).read()
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
            search_results.write("Where I found it: http://imgur.com/gallery/" + galleryName + "\n" + "\n")
            search_results.write("Google Results:\n" + "------------------\n")
            if (len(findBestGuess) > 0):
                bestGuess = string.replace(findBestGuess[0], '+', ' ')
                search_results.write("Google best guess: " + bestGuess + "\n" + "\n")
            search_results.write("Pages containing image:\n")
            for url in findLinks:
                search_results.write(url + "\n")
            search_results.write("\n")
        search_results.close()


def APILookup(client, filename):
    imageID = os.path.splitext(filename)[0]

    print ("Looking for info from Imgur...")
    print (imageID)
    gallery_obj = client.gallery_item(imageID)

    with open('search_results.txt', 'a') as search_results:
        search_results.write("Imgur search:\n" + "------------------\n")
        if (gallery_obj.title is not None):
            search_results.write("title: " + gallery_obj.title + "\n")
        search_results.write("owner: " + gallery_obj.account_url + "\n")
        # Convert epochtime from imgur to human readable
        post_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(gallery_obj.datetime))
        search_results.write("date: " + post_date + "\n" + "\n")
        if (gallery_obj.description is not None):
            search_results.write("description: " + gallery_obj.description + "\n")
        search_results.write("views: " + str(gallery_obj.views) + "\n")
        search_results.write("upvotes: " + str(gallery_obj.ups) + "\n")
        search_results.write("downvotes: " + str(gallery_obj.downs) + "\n")
        search_results.write("score: " + str(gallery_obj.score) + "\n")
    search_results.close()
    print ("done.")


def LookupUrl(client):
    request_obj = client.get_notifications()
    messages = request_obj['messages']
    if (len(messages) > 0):
        new_message = messages[0].content  # Just pull the first unread
        print ((new_message['last_message']))
        # Search new message for imageID
        match_obj = re.search(r'http://imgur.com/gallery/(.*?)/comment/',
                          new_message['last_message'])
        matches = match_obj.groups()
        if (len(matches) > 0):
            imageID = string.replace(matches[0], '/', '')
            print (("ImageID: " + imageID))

    img_obj = client.get_image(imageID)
    filename = string.replace(img_obj.link, 'http://i.imgur.com/', '')
    print (filename)
    UserLookup(filename)


def UserLookup(filename):
    if (filename.endswith('webm')):
        with open('search_results.txt', 'w') as search_results:
            search_results.write("Google Reverse image lookup does not support this file format \n" + "\n")
    else:
        print ("")
        print ("Attempting reverse image search")
        # Also check to see if image was removed
        # path to file on imgur server
        remotepath = 'http://i.imgur.com/' + filename
        # url to perform reverse image search
        googlepath = 'http://www.google.com/searchbyimage?image_url=' + remotepath
        # Visit the url provided
        sourceCode = opener.open(googlepath).read()
        # Parse output of search (.*? handles any output after regex)
        # Links to pages containing the image
        findLinks = re.findall(r'<div class="rc" data-hveid=".*?">.*?imgurl=(.*?)&amp;', sourceCode)
        # Googles best guess for related keywords (title generation?)
        findBestGuess = re.findall(r'<div class="_hUb">.*?q=(.*?)&amp;', sourceCode)
        # Write results to file for use in description
        print ("")
        print ("Search complete, saving results")
        with open('search_results.txt', 'w') as search_results:
            search_results.write("Search by image URL: " + ShortenUrl(googlepath) + "\n")
            if (len(findBestGuess) > 0):
                bestGuess = string.replace(findBestGuess[0], '+', ' ')
                search_results.write("Google best guess: " + bestGuess + "\n" + "\n")
            search_results.write("Pages containing image:\n")
            for url in findLinks:
                search_results.write(url + '\n')
        search_results.close()


def ShortenUrl(url):
    # Get APIKey from auth.ini
    config = get_config()
    config.read('auth.ini')  # this is the file that holds user credentials
    api_key = config.get('credentials', 'api_key')

    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + api_key
    postdata = {'longUrl': url}
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request(
        post_url,
        json.dumps(postdata),
        headers)
    ret = urllib2.urlopen(req).read()

    return json.loads(ret)['id']