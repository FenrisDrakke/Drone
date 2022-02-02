from djitellopy import tello
import cv2

drone = tello.Tello()
# connect take care of the communication
drone.connect()
print(drone.get_battery())

drone.streamon()

while True:
    image = drone.get_frame_read().frame
    # resize the image for faster and more stable stream
    Image = cv2.resize(image,(360,240))
    # imshow creates a window
    cv2.imshow("Stream", image)
    # keeps open the window
    cv2.waitKey(1)
