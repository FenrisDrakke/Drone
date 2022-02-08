import cv2
from djitellopy import tello
import keyboard_control as kc
import numpy as np
import math
from time import sleep

# mesured data with drone
fspeed = 118 / 10  # forwared speed cm/s (15cm/s)
aspeed = 360 / 10  # angular speed degrees/s (50d/s)
interval = 0.25

dInterval = fspeed * interval
aInterval = aspeed * interval

x, y = 500, 500
a = 0  # Angle
yaw = 0

kc.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

points = []


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    # use velocity 50 for testing
    velocity = 15
    avelocity = 50
    global x, y, yaw, a
    d = 0

    if kc.getkey("a"):
        lr = -velocity
        d = dInterval
        a = -180
    elif kc.getkey("d"):
        lr = velocity
        d = -dInterval
        a = 180

    if kc.getkey("w"):
        fb = velocity
        d = dInterval
        a = 270
    elif kc.getkey("s"):
        fb = -velocity
        d = -dInterval
        a = -90

    if kc.getkey("UP"):
        ud = velocity
    elif kc.getkey("DOWN"):
        ud = -velocity

    if kc.getkey("LEFT"):
        yv = -avelocity
        yaw -= aInterval
    elif kc.getkey("RIGHT"):
        yv = avelocity
        yaw += aInterval

    if kc.getkey("q"):
        drone.land()
    elif kc.getkey("e"):
        drone.takeoff()

    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoint(image, points):
    for point in points:
        cv2.circle(image, point, 5, (0, 0, 255), cv2.FILLED)
        # color is in BGR blue-green-red
    cv2.circle(image, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(image, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    # /100 makes it to be mesuared in maters not in centimeters


while True:
    val = getKeyboardInput()
    drone.send_rc_control(val[0], val[1], val[2], val[3])

    image = np.zeros((1000, 1000, 3), np.uint8)
    points.append((val[4], val[5]))
    drawPoint(image, points)
    cv2.imshow("output", image)
    cv2.waitKey(1)
