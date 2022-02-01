from djitellopy import tello
import cv2

me = tello.Tello()
# connect take care of the communication
me.connect()
print(me.get_battery())

me.streamon()

while True:
      image = me.get_frame_read().frame
      # resize the image for faster and more stable stream
      Image = cv2.resize(image,(360,240))
      # imshow creates a window
      cv2.imshow("Drones image", image)
      # keeps open the window
      cv2.waitkey(1)
