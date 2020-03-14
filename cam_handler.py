import sys
import json
from datetime import datetime
from visca import camera

def handleCommand(cam, args):
    if command == 'home':
        cam.home()

# Code to execute:
cam = camera.D30(output='COM3', deaf=1)
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