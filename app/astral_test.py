import camera

cam = camera.D30(output='/dev/tty.usbserial-140')
cam.init()
cam.home()
