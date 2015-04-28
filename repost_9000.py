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
toaddrs = 'codiferus17@gmail.com'

# Empty directory array
files = None

# Path to target source directory
folder = '/home/cody/repost_9000/images'

# Path to currently selected image
path = None
filename = None


def PostToMail(ImgFileName):
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
    global path
    global filename
    index = GetRandom()
    print (("Selected index ", index))
    filename = files[index]
    path = folder + "/" + files[index]  # External directory
    return path


def TestEmailPost():
    FillArray(folder)
    rand_image = FindRandomImage()
    PostToMail(rand_image)


def TestAPIPost():
    client = StartClient()
    FillArray(folder)
    rand_image = FindRandomImage()
    MakePost(client, rand_image)
    EmailNotify(toaddrs)


def EmailNotify(UserEmail):
    msg = MIMEMultipart()
    msg['Subject'] = 'repost_9000 activity log'
    msg['From'] = fromaddr
    msg['To'] = UserEmail

    text = MIMEText("repost_9000 has posted an image to Imgur")
    msg.attach(text)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    print (("sending confirmation to " + UserEmail))
    server.sendmail(fromaddr, UserEmail, msg.as_string())
    print ("successful...")
    server.quit()


def RemoveImage():
    print("adding file to list of posted images")
    with open('posted_files.txt', 'a') as file_log:
        file_log.write(filename)
    print("removing posted image from directory")
    #os.remove(path)  # Option to delete the file from candidate directory


#TestEmailPost()
TestAPIPost()
RemoveImage()