import os
import sys
repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
visca_path = os.path.join(repo_path, "visca")
sys.path.insert(0, visca_path)
import camera

cam = camera.D30(output='/dev/ttyUSB0', deaf=1)
cam.init()

cam.set_cam_ae_bright()
print("Cam adjust brightness utility.")
print("Entering manual brightness mode.")
print('Input = "u" for up, "d" for down, "r" for reset, "q" for quit, "a" for auto.')
while True:
    adjust = input("Input = ")
    if adjust == "u":
        cam.set_bright_up()
    elif adjust == "d":
        cam.set_bright_down()
    elif adjust == "r":
        cam.set_bright_reset()
    elif adjust == "q":
        print("Goodbye.")
        break
    elif adjust == "a":
        print("Entering auto brightness mode.")
        cam.set_cam_ae_auto()
        while True:
            accept = input('Accept? y/n ')
            if accept == "y" or accept == "q":
                print("Goodbye.")
                break
            elif accept == "n":
                print("Re-entering manual brightness mode.")
                cam.set_cam_ae_bright()
                break
            else:
                print("Unknown command.")
        if accept == "y" or accept == "q":
            break
    else:
        print("Unknown command.")