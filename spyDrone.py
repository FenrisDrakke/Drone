import time
from djitellopy import tello
import keyboard_control as kc
import cv2

global image

kc.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.streamon()


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    # use velocity 50 for testing
    velocity = 100

    if kc.getkey("a"):
        lr = -velocity
    elif kc.getkey("d"):
        lr = velocity

    if kc.getkey("w"):
        fb = velocity
    elif kc.getkey("s"):
        fb = -velocity

    if kc.getkey("UP"):
        ud = velocity
    elif kc.getkey("DOWN"):
        ud = -velocity

    if kc.getkey("LEFT"):
        yv = -velocity
    elif kc.getkey("RIGHT"):
        yv = velocity

    if kc.getkey("q"):
        drone.land()
        time.sleep(1)
    elif kc.getkey("e"):
        drone.takeoff()

    if kc.getkey('f'):
        cv2.imwrite(f'C:/Users/Bence/PycharmProjects/Scriba/Drone/Images/{time.time()}.jpg', image)
        time.sleep(0.1)

    return [lr, fb, ud, yv]


while True:
    val = getKeyboardInput()
    drone.send_rc_control(val[0], val[1], val[2], val[3])
    image = drone.get_frame_read().frame
    # resize the image for faster and more stable stream
    Image = cv2.resize(image, (360, 240))
    # imshow creates a window
    cv2.imshow("Stream", image)
    # keeps open the window
    cv2.waitKey(1)
