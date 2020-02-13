# https://bottlepy.org/docs/dev/tutorial.html

from visca import camera
from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=8080, debug=True)

# cam = camera.D30(output='COM3')
# cam.init()