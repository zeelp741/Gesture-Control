import cv2
import mediapipe as mp
import time
import pandas as pd
import keyboard


class HandDetector():
    def __init__(self, mode = False, maxHands = 2, detectionConfidence = 0.5, trackConfidence = 0.5):
        # Default Values
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionConfidence
        self.trackCon = trackConfidence

        # Draws Hand
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

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
        landMarksList = []

        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks[handNum]

            for id, landMarks in enumerate(hands.landmark):
                # print(id, landMarks)
                height, width, channels = img.shape
                cx, cy = int(landMarks.x * width), int(landMarks.y * height)
                # print(id, cx, cy)

                landMarksList.append([id, cx, cy])

                if draw == True and id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 255, 255), cv2.FILLED)
        
        return landMarksList

def fps(img, prevTime, currTime, WIDTH, HEIGHT):
    # Calculates the FPS
    currTime = time.time()
    fps  = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(img, "FPS: " + str(int(fps)), (int(WIDTH - 200) , 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    return prevTime, currTime

def webcamResolution(capture):
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

    print(resolutions)
    
    return resolutions

def displayResolution(img, resolutions, WIDTH, HEIGHT):
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

    resolutions = webcamResolution(capture)
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

        prevTime, currTime = fps(img, prevTime, currTime, WIDTH, HEIGHT)
        displayResolution(img, resolutions, WIDTH, HEIGHT)

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