import cv2
import time
import numpy as np 
import HandTracking as ht
from HandTracking import fps, webcamResolution, displayResolution
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

hand_detector = ht.HandDetector(detectionConfidence = 0.7)

# Volume variables
vol = 0
volBar = 400
volPer = 0

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

    img = hand_detector.locateHands(img)
    landMarkList = hand_detector.locatePosition(img, draw = False)

    if len(landMarkList) > 0 :

        x1, y1 = landMarkList[4][1], landMarkList[4][2]
        x2, y2 = landMarkList[8][1], landMarkList[8][2]
        lmx, lmy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (lmx, lmy), 15, (255, 255, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2), (255, 255, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Volume Range is between -65 - 0

        vol = np.interp(length, [20, 200], [minVolume, maxVolume])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(length, vol)
        volume.SetMasterVolumeLevel(vol, None)



        if length < 20:
            cv2.circle(img, (lmx, lmy), 15, (0, 0, 255), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        







    

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)