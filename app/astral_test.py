import camera

cam = camera.D30(output='/dev/ttyUSB0')
cam.init()
cam.home()
