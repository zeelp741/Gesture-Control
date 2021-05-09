import cv2
import mediapipe as mp
import time
import pandas as pd
import keyboard
import math


class HandDetector():
    def __init__(self, mode = False, maxHands = 2, detectionConfidence = 0.5, trackConfidence = 0.5):
        # Default Values
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        # Draws Hand
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.fingerTipID = [4, 8, 12, 16, 20]

    def locateHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
            
        # Draws Landmarkers on Hands if detected
        if self.results.multi_hand_landmarks:
            for handLandMarks in self.results.multi_hand_landmarks:
                if draw == True:
                    self.mpDraw.draw_landmarks(img, handLandMarks, self.mpHands.HAND_CONNECTIONS)

        return img

    def locatePosition(self, img, handNum = 0, draw = True):
        xList = []
        yList = []
        boundingBox = []


        self.landMarksList = []

        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks[handNum]

            for id, landMarks in enumerate(hands.landmark):
                # print(id, landMarks)
                height, width, channels = img.shape
                cx, cy = int(landMarks.x * width), int(landMarks.y * height)

                xList.append(cx)
                yList.append(cy)

                # print(id, cx, cy)

                self.landMarksList.append([id, cx, cy])

                if draw == True and id == 8:
                    cv2.circle(img, (cx, cy), 5, (255, 255, 255), cv2.FILLED)

            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)
            boundingBox = xMin, yMin, xMax, yMax

            if draw == True:
                cv2.rectangle(img, (boundingBox[0] - 20, boundingBox[1] - 20 ),  (boundingBox[2] + 20, boundingBox[3] + 20), (0, 255, 0), 2)
        
        return self.landMarksList, boundingBox

    def calculateDistance(self, p1, p2, img, draw = True):
        x1, y1 = self.landMarksList[p1][1], self.landMarksList[p1][2]
        x2, y2 = self.landMarksList[p2][1], self.landMarksList[p2][2]
        
        lmx, lmy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw == True:
            cv2.circle(img, (x1, y1), 15, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (lmx, lmy), 15, (255, 255, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2,y2), (255, 255, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, lmx, lmy]

    def fingersUp(self):
        fingers  = []

        # Thumb
        if self.landMarksList[self.fingerTipID[0]][1] > self.landMarksList[self.fingerTipID[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # 4 Fingers

        for id in range(1, 5):
            if self.landMarksList[self.fingerTipID[id]][2] < self.landMarksList[self.fingerTipID[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


    def fps(self, img, prevTime, currTime, WIDTH, HEIGHT):
        # Calculates the FPS
        currTime = time.time()
        fps  = 1 / (currTime - prevTime)
        prevTime = currTime
        cv2.putText(img, "FPS: " + str(int(fps)), (int(WIDTH - 200) , 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

        return prevTime, currTime

    def webcamResolution(self, capture):
        # Checks possible webcams
        url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
        table = pd.read_html(url)[0]
        table.columns = table.columns.droplevel()

        resolutions = {}

        for index, row in table[["W", "H"]].iterrows():
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, row["W"])
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, row["H"])
            width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            resolutions[str(width)+" x "+str(height)] = "OK"
    
        return resolutions

    def displayResolution(self, img, resolutions, WIDTH, HEIGHT):
        cv2.putText(img, "Res: " + str(list(resolutions)[-1]), (int(WIDTH - 520) , 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)


def main():

    #  Varibles
    prevTime = 0
    currTime = 0

    capture = cv2.VideoCapture(0)
    hand_detector = HandDetector()

    # Webcam Dimensions
    WIDTH = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    resolutions = hand_detector.handwebcamResolution(capture)
    print(resolutions)

    while True:

        WIDTH = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        HEIGHT = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        success, img = capture.read()

        img = hand_detector.locateHands(img)
        landMarkList  = hand_detector.locatePosition(img)

        if len(landMarkList ) != 0:
            pass
            # print(lmList[4])

        prevTime, currTime = hand_detector.fps(img, prevTime, currTime, WIDTH, HEIGHT)
        hand_detector.displayResolution(img, resolutions, WIDTH, HEIGHT)

        try: 
            if keyboard.is_pressed('q'):  
                print("Program executed")
                break 
        except:
            break  

        cv2.imshow("Webcam", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()