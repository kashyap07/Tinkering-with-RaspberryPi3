'''
Home Automation System
'''
from flask import Flask, render_template, request, jsonify, abort
from flask_sse import sse
import os
import json
import requests
from pprint import pprint

import RPi.GPIO as GPIO
import time

from threading import Timer


# init flask application
app = Flask(__name__)

# redis
app.config['REDIS_URL'] = 'redis://localhost'
# sse
app.register_blueprint(sse, url_prefix='/stream')


# global var
is_on = False
timer = None


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


# raspberry pi camera route
@app.route('/sendphoto', methods=['POST'])
def sendphoto():
	file = request.files['image']
	file.save('../test.jpg')

	print('saved image test.jpg')



@app.route('/remote')
def gpio():
	print('rendering remote gpio control page')

	return render_template('remote.html')


# -----------------------------------------------------------------------------

@app.route('/switch')
def switch():
	global is_on
	global timer

	val = request.args.get('on')
	if val=="True":
		if is_on:
			timer.cancel()
		else:
			turn_on()
			is_on = True

		timer = Timer(time_threshold, sse_turn_off)
		timer.start()
	elif val=="False":
		turn_off()
		is_on = False

	return render_template('blank.html')


def turn_on():
	print('LED ON')
	GPIO.output(18, GPIO.HIGH)


def turn_off():
	print('LED OFF')
	GPIO.output(18, GPIO.LOW)


def sse_turn_off():
	global is_on

	turn_off()
	is_on = False

	# sse
	with app.app_context():
		sse.publish({'success': 'True'}, type='success')

# -----------------------------------------------------------------------------

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