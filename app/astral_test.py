import os
import sys
repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
visca_path = os.path.join(repo_path, "visca")
sys.path.insert(0, visca_path)
import camera

cam = camera.D30(output='/dev/ttyUSB0')
cam.init()
cam.home()