from visca import camera
cam = camera.D30(output='COM3')
cam.init()

# import binascii

# def test(cam, read=3):
#     # cam._output.write(binascii.unhexlify('81010604FF'))
#     response = binascii.hexlify(cam._output.read(read))
#     return response

# from time import sleep

# cam = camera.D100(output='COM3') # set serial port
# cam.init() # initialize camera object and connect to serial port

# input("Press enter to home!")
# # Now you can run commands
# cam.home() # send camera to home position
# input("It should have just homed! Now let's do more stuff...")
# cam.right(amount=10)
# sleep(1)
# cam.stop()
# input("Next it will go until you hit stop...")
# cam.left()
# input("Press enter to stop.")
# cam.stop()