# -*- coding: utf-8 -*-

# contact: cody.rocker.83@gmail.com

"""

Meant to select a random image from a directory of images I've downloaded for various
reasons, then repost it through the public Imgur Python API.

"""

# IDEAS
# ---------------
# + First
#    Get the script running and producing reliably random output
# + Second
#    Automate posting through the API
# + Third
#    credit original post via reverse image search under the imgur domain
#    http://stackoverflow.com/questions/13662667/sending-get-requests-for-a-google-reverse-image-search
#    https://developers.google.com/api-client-library/python/apis/customsearch/v1

# Writted for Python 2.7.9
import os, sys, time, platform
from random import randint

# Requires Imgur's Python api to be installed. >> https://github.com/Imgur/imgurpython
from imgurpython import ImgurClient