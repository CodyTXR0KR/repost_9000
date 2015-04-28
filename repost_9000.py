# -*- coding: utf-8 -*-

# contact: cody.rocker.83@gmail.com
# http://imgur.com/user/repost9000

import os
import smtplib  # python builtin email handler

from random import randint

# Email dependancies
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Requires Imgur's Python api to be installed. >> https://github.com/Imgur/imgurpython
# Documentation >> https://api.imgur.com/
from imgur_client import StartClient, MakePost
from helpers import get_config

# Get email username and password from auth.ini
config = get_config()
config.read('auth.ini')  # this is the file that holds user credentials
username = config.get('credentials', 'username')
password = config.get('credentials', 'password')

# Routing addresses
fromaddr = username
toaddrs = 'upload@imgur.com'

# Empty directory array
files = None

# Path to target source directory
folder = '/home/cody/repost_9000/images'


def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Test'
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    text = MIMEText("This image was randomly selected")
    msg.attach(text)
    if ImgFileName.endswith(".png"):
        image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    elif ImgFileName.endswith(".gif"):
        image = MIMEImage(img_data, 'gif', name=os.path.basename(ImgFileName))
    elif ImgFileName.endswith(".jpg"):
        image = MIMEImage(img_data, 'jpg', name=os.path.basename(ImgFileName))
    else:
        print ("media type not supported...aborting.")
        exit
    msg.attach(image)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    print (("attempting to send " + ImgFileName + " to " + toaddrs))
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    print ("successful...")
    server.quit()


def FillArray(Folder):
    global files
    if files is None:
        print ("Populating array...")
        files = os.listdir(Folder)
        print (("Found ", len(files), " images."))
    else:
        return


def GetRandom():
    global files
    return randint(0, len(files))


def FindRandomImage():
    index = GetRandom()
    print (("Selected index ", index))
    path = folder + "/" + files[index]  # External directory
    return path


def TestEmailPost():
    FillArray(folder)
    rand_image = FindRandomImage()
    SendMail(rand_image)


def TestAPIPost():
    client = StartClient()
    FillArray(folder)
    rand_image = FindRandomImage()
    MakePost(client, rand_image)


#TestEmailPost()
TestAPIPost()