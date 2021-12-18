from flask import Flask
from flask import request
from flask.json import jsonify
app = Flask(__name__)
import json

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pins=[2,4,15,22]
GPIO.setup(pins,GPIO.OUT)
GPIO.output(pins,GPIO.HIGH)


@app.route('/on', methods = ['POST'])
def on():
            GPIO.output(4, GPIO.LOW)
            time.sleep(5)
            GPIO.output(4, True)
            x = '{"led":"on"}'
            y = json.loads(x)
            return y
            # return jsonify(y)
    
@app.route('/off', methods = ['POST'])
def off():
            GPIO.output(4, GPIO.HIGH)
            x = '{"led":"off"}'
            y = json.loads(x)
            return y
            # return jsonify(y)
    
@app.route('/door', methods = ['POST'])
def door():
            open = request.json
            GPIO.output(15, GPIO.LOW)
            GPIO.output(2,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(15,GPIO.HIGH)
            GPIO.output(2,GPIO.HIGH)
            time.sleep(6.5)
            GPIO.output(22,GPIO.HIGH)
            return jsonify({"status": "ok"})
            # open = json.loads(open)
            # return open

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=8000)