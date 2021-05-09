import cv2
import time
import numpy as np 
import HandTracking as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Dimensions
webcamWidth = 1280
webcamHeight = 720

# Webcam Setup 
capture = cv2.VideoCapture(0)
capture.set(3, webcamWidth)
capture.set(4, webcamHeight)

# Webcam Dimensions
WIDTH = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHT = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Hand object
hand_detector = ht.HandDetector(detectionConfidence = 0.7)

# Volume variables
vol = 0
volBar = 400
volPer = 0
boundingBoxArea = 0

# Setup Core Audio Windows Library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()


minVolume = volumeRange[0]
maxVolume = volumeRange[1]




while True:

    # TODO
    # Add FPS and resolution 
    success, img = capture.read()

    # Find Hand
    img = hand_detector.locateHands(img)
    landMarkList, boundingBox = hand_detector.locatePosition(img, draw = True)

    if len(landMarkList) > 0 :

        boundingBoxArea = (boundingBox[2] - boundingBox[0]) * (boundingBox[3] - boundingBox[1]) // 100
        if boundingBoxArea > 100 and boundingBoxArea < 500:

            # Distance between index and thumb
            length, img, lineDetails = hand_detector.calculateDistance(4, 8, img)
            # print(length)

            # Convert Volume 
            # vol = np.interp(length, [20, 200], [minVolume, maxVolume])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])

            # Makes Bar smooth
            smoothness = 5
            volPer = smoothness * round(volPer / smoothness)

            # Detect Fingers up
            fingers = hand_detector.fingersUp()
            # print(fingers)

            # Detect if Ring Finger is up
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (lineDetails[4], lineDetails[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

            # if length < 20:
            #     cv2.circle(img, (lmx, lmy), 15, (0, 0, 255), cv2.FILLED)


            # Volume Range is between -65 - 0

        # Drawings
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3) 
        cVol = int(volume.GetMasterVolumeLevelScalar() * 100)           




    cv2.imshow("Webcam", img)
    cv2.waitKey(1)