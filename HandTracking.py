import cv2 
import mediapipe as mp 
import time

capture = cv2.VideoCapture(0)

mpHands = mp.solutions.hands

# Default values
# static_image-Mode = False, max_nim_hands = 2, min_detection_confidence = 0.5, min_tracking_confidence = 2
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils


while True:
    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Detects Hand
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLandMarks in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLandMarks)



    cv2.imshow("Video", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

