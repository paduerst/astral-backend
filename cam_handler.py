import sys
import json
from datetime import datetime
from visca import camera

def handleCommand(cam, args):
    command = args[0]
    val1 = args[1]
    val2 = args[2]
    if command == 'home':
        cam.home()

# Code to execute:
cam = camera.D30(output='COM4', deaf=1)
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