import time

import cv2
import numpy as np
from djitellopy import tello

drone = tello.Tello()
# connect take care of the communication
drone.connect()
print(drone.get_battery())

drone.streamon()
drone.takeoff()
drone.send_rc_control(0, 0, 25, 0)
time.sleep(2)

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0


def findFace(Image):
    faceCascade = cv2.CascadeClassifier(
        "C:/Users/Bence/PycharmProjects/Scriba/Drone/haarcascade_frontalface_default.xml")
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imageGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    # too find the center of the face and create the frame
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(image, (cx, cy), 5, [0, 255, 0], cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return image, [myFaceListC[i], myFaceListArea[i]]
    else:
        return image, [{0, 0}, 0]


def trackFace(drone, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)
    drone.send_control(0, fb, 0, speed)
    return error


# cap = cv2.VideoCapture(0)

while True:
    # use of the webcam for testing with unstable wireless connection
    # _, image = cap.read()
    image = drone.get_frame_read().frame
    image = cv2.resize(image, (w, h))
    image, info = findFace(image)
    pError = trackFace(drone, info, w, pid, pError)
    # print("Area", info[1], "Center", info[0])
    cv2.imshow("Camera feed", image)
    # 0xFF is a bit mask which sets the left 24 bits to zero
    #  ord() returns a value between 0 and 255
    if cv2.waitKey(1) and 0xFF == ord('q'):
        drone.land()
        break
