import face_recognition
import cv2
import numpy as np
import time
import re
import pyautogui as auto
import pyperclip
from mongoConnection import MongoConnect

blackPersonList = []
blackUrlList = []

def hotkeyCtrl(c):
    auto.keyDown('ctrl')
    auto.keyDown(c)
    auto.keyUp(c)
    auto.keyUp('ctrl')

def getCurrentUrl():
    auto.click(300, 70)
    hotkeyCtrl('a')
    hotkeyCtrl('c')
    return pyperclip.paste()

def nextTab():
    hotkeyCtrl('tab')

def closeTab():
    hotkeyCtrl('w')

def goClose():
    auto.PAUSE = 0.01
    chromeWindow = auto.getWindowsWithTitle('Google Chrome')[0]
    chromeWindow.maximize()
    chromeWindow.activate()

    # go to next tab
    # click -> ctrl A -> copy -> verify
    # close and loop or end

    originalUrl = getCurrentUrl()
    closed = False

    while True:
        if not closed:
            nextTab()
        closed = False
        theUrl = getCurrentUrl()
        for site in blackUrlList:
            if site in theUrl:
                closeTab()
                closed = True
                break
        if theUrl == originalUrl:
            break


#initialize the list of blocked person
mongo = MongoConnect()
mongo.initDb()
mongo.getImages()
blackPersonList = mongo.ImageList

#initialize the list of blocked urls
mongo.getURLs()
tempList = mongo.URLlist
for item in tempList:
    blackUrlList.append(item.get('url'))

video_capture = cv2.VideoCapture(0)

# imageList = ("img/chris.jpg", "img/lucy.jpg")

images = []
for imgFile in blackPersonList:
    images.append(face_recognition.load_image_file(imgFile))

known_face_encodings = []
for image in images:
    known_face_encodings.append(face_recognition.face_encodings(image)[0])

known_face_names = []
for name in blackPersonList:
    known_face_names.append(re.sub('.*/(.*)\..*', '\\1', name))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

scale = 1

while True:
    time.sleep(1)
    # Grab a single frame of video
    ret, frame = video_capture.read()


    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
##        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
##        best_match_index = np.argmin(face_distances)
##        if matches[best_match_index]:
##            name = known_face_names[best_match_index]

        face_names.append(name)

    
    for name in face_names:
        if name in known_face_names:
            goClose()

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
