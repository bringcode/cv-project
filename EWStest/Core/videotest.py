import picamera
import time

with picamera.PiCamera() as camera:
    camera.resolution = (800, 600)
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()