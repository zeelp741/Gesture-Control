# Gesture-Control
https://user-images.githubusercontent.com/48848450/117927960-e9c2e780-b2c8-11eb-879a-a5833fdd2f55.mp4


## Inspiration 
Computer vision in becoming a more and more in-demand field as many different fields are currently using this techonology such as self driving cars and industrial automation. The inspiration for this project came when I first sat in a Tesla recently and saw the self-driving feature activated. This was really inspiring and motivated me to learn the OpenCV library. This led me to create a music controller which uses the webcam to change the volume of the device and also play/pause and skip/repeat songs. 

## Technologies 
- Open CV:
  -  get webcam input
  -  alter image before getting hand detection
  -  display hand landmarks
- Mediapipe
  -  detect hand landmarks  
- Pandas
  - check webcam resolution 


## Features
- Increase and decrease sound 
- Play and pause music
- skip and repeat song


## Hand Detection
![hand](https://user-images.githubusercontent.com/48848450/117922556-ab292f00-b2c0-11eb-89b4-db6665c240ef.png)

## Demo
![hand3](https://user-images.githubusercontent.com/48848450/117927526-5093d100-b2c8-11eb-8886-f92724ff4602.png)

https://user-images.githubusercontent.com/48848450/117927437-3528c600-b2c8-11eb-8d44-c61c2032eb88.mp4

To change volume
- put hand in frame until thumb and index finger connect with a line
- while in this mode volume change will be showed but not executed
- put down ring ringer, middle circle should turn green
- moving finger and thumb further and closer together will change the system volume 



