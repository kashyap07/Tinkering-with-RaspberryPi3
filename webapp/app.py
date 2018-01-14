'''
Home Automation System
'''


from flask import Flask, render_template, request, jsonify, abort
import os
import json
import requests
from pprint import pprint

import RPi.GPIO as GPIO
import time

from threading import Timer


# init flask application
app = Flask(__name__)


# index route
@app.route('/')
def index():
	data = request.get_json()

	print(data)

	return render_template('index.html')

# camera page web view
@app.route('/viewphoto')
def camera():
	

	return render_template('view.html')

# raspberry pi casmera route
@app.route('/sendphoto', methods=['POST'])
def sendphoto():
	file = request.files['image']
	file.save('../test.jpg')

	print('saved image test.jpg')



@app.route('/remote')
def gpio():
	print('rendering remote gpio control page')

	return render_template('remote.html')


@app.route('/turnon')
def turn_on():
	print('LED ON')
	GPIO.output(18, GPIO.HIGH)

	timer = Timer(time_threshold, turn_off)
	timer.start()

	return 200


@app.route('/turnoff')
def turn_off():
	print('LED OFF')
	GPIO.output(18, GPIO.LOW)

	return 200



if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(18, GPIO.OUT)

	time_threshold = 5

	app.run(
		threaded=True,
		debug=True,
		host='0.0.0.0',
		port=8000
	)