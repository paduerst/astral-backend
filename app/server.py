from flask import Flask, request, abort, send_from_directory
from flask_cors import CORS

import camera
from cam_handler import handle_command


app = Flask(__name__)
CORS(app)

cam = None


@app.route('/', methods=['GET'])
def handle_root_get():
    if request.args.get("command") and cam is not None:
        command_args = [
            request.args.get("command"),
            request.args.get("val1"),
            request.args.get("val2")
        ]
        handle_command(cam, command_args)
    return "Hello, website!"


if __name__ == '__main__':
    cam = camera.D30(deaf=True)
    try:
        cam.init()
    except:
        cam = None
    app.run(port=8080, debug=True)
