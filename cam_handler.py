import sys
import json

args = sys.argv[1:]

with open('log.txt', 'a') as log:
    log.write(str(args))
    log.write('\n')

message_back = {
    'args': args,
    'message': """Hello!
This is a return json message.
That is all."""
}

print(json.dumps(message_back))