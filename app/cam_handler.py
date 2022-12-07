import os
import sys
repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
visca_path = os.path.join(repo_path, "visca")
sys.path.insert(0, visca_path)
import camera

import json
from datetime import datetime

def handleCommand(cam, args):
    command = args[0]
    val1 = args[1]
    val2 = args[2]
    if command == 'home':
        cam.home()
    elif command == 'pantilt' or command == 'relpantilt':
        pan = int(val1)/97.0
        tilt = int(val2)/32.0
        if command == 'relpantilt':
            shift = 1
        else:
            shift = 0
        cam.set_pos(pan=pan, tilt=tilt, shift=shift)
    elif command == 'zoom':
        percentage = int(val1)/100.0
        cam.set_zoom(percentage)
    elif command == 'mem':
        if val1 == 'goto':
            action = 2
        elif val1 == 'set':
            action = 1
        address = int(val2)-1
        cam.memory(address, action)

# Code to execute:
cam = camera.D30(output='/dev/ttyUSB0', deaf=1)
cam.init()

args = sys.argv[1:]

with open('log.txt', 'a') as log:
    log.write(datetime.now().strftime('(%Y-%m-%d, %H:%M:%S): '))
    log.write(str(args))
    log.write('\n')

handleCommand(cam, args)

message_back = {
    'args': args,
    'message': 'Python: Success!'
}

print(json.dumps(message_back))