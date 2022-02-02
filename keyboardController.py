from djitellopy import tello
import keyboard_control as kc
from time import sleep

kc.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())


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
    elif kc.getkey("e"):
        drone.takeoff()

    return [lr, fb, ud, yv]


while True:
    val = getKeyboardInput()
    drone.send_rc_control(val[0], val[1], val[2], val[3])
    sleep(0.05)
    # sleep to slow down the imput for testing
