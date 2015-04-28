# -*- coding: utf-8 -*-

#from auth import authenticate  # for failed authentication check later
from helpers import get_config
from imgurpython import ImgurClient

# Need a check to make sure the refresh_token exists


def StartClient():
    # Get credentials from auth.ini
    config = get_config()
    config.read('auth.ini')  # this is the file that holds user credentials
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    refresh_token = config.get('credentials', 'refresh_token')

    # Start client
    client = ImgurClient(client_id, client_secret, None, refresh_token)
    return client


def MakePost(client, image):
    meta = {'album': None,
            'name': None,
            'title': 'Hello World',
            'description': 'This image was selected randomly and uploaded, '
                           'automatically, as a test using Imgur PythonAPI.  '
                           'More info can be found in user profile'}

    print ("")
    print (("Attempting to upload file: " + image))
    client.upload_from_path(image, meta, anon=False)
    print ("")
    print ("Success...")