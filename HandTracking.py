import cv2 
import mediapipe as mp 
import time
import pandas as pd
import keyboard

capture = cv2.VideoCapture(0)

# Global Varibles
prevTime = 0
currTime = 0

# Webcam Dimensions
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

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


mpHands = mp.solutions.hands            # static_image-Mode = False, max_nim_hands = 2, min_detection_confidence = 0.5, min_tracking_confidence = 2
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def fps(prevTime, currTime):
    # Calculates the FPS
    currTime = time.time()
    fps  = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(img, "FPS: " + str(int(fps)), (int(width - 200) , 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    cv2.putText(img, "Res: " + str(list(resolutions)[-1]), (int(width - 520) , 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    return prevTime, currTime

while True:

    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    prevTime, currTime = fps(prevTime, currTime)

    # Detects Hand
    # print(results.multi_hand_landmarks)

    # Draws Landmarkers on Hands if detected
    if results.multi_hand_landmarks:
        for handLandMarks in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLandMarks, mpHands.HAND_CONNECTIONS)

    # Exits program 
    try: 
        if keyboard.is_pressed('q'):  
            break 
    except:
        break  

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

