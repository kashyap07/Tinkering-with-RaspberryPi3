'''
renote applicances
'''
from flask import Flask, render_template, request, jsonify, abort
import os
import json
import requests

import RPi.GPIO as GPIO
import time


# init flask application
app = Flask(__name__)


# index route
@app.route('/')
def index():
	data = request.get_json()

	print(data)

	return render_template('index.html')




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

print('LED ON')
GPIO.output(18, GPIO.HIGH)
time.sleep(1)

print('LED OFF')
GPIO.output(18, GPIO.LOW)
