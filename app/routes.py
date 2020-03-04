from flask import request, jsonify
from app import app

def doRequest():
    pass

@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    json_data = request.get_json()
    print(json_data)
    return jsonify(result='success', shortUrl='BLARG')