import flask
import requests
import json
from flask import request, jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/test', methods=['GET'])
def home():
    name = 'someone'
    body = {"url": "http://<doorbird username>:<Doorbird PAssword>@<DoorBird IP>:80/bha-api/image.cgi","faceprint": "false"}
    head = {'Content-Type' : 'application/json'}
    resp = requests.post('http://<Facebox IP>:8080/facebox/check/', json=body, headers=head)
    if resp.status_code == 200:
        data = json.loads(resp.content.decode('utf-8'))
        if data['facesCount'] > 0:
            for index in data['faces']:
                print(index)
                if index['matched']==True:
                    name = index['name']
                    break
    body = {"state": name, "attributes": {"friendly_name": "Person Name"}}
    head = {'Content-Type' : 'application/json','Authorization' : 'Bearer <HA Long Term Token>'}
    resp = requests.post('http://<HA IP>:8123/api/states/sensor.face', json=body, headers=head)
    return '1'
app.run()
