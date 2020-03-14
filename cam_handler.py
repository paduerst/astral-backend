import sys
import json

args = sys.argv[1:]

with open('log.txt', 'a') as log:
    log.write(str(args))
    log.write('\n')

message_back = {
    'args': args,
    'message': 'This is a message from the Python script!'
}

print(json.dumps(message_back))