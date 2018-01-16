'''
Home Automation System
'''
from flask import Flask, render_template, request, jsonify, abort
from flask_sse import sse
import os
import sys
import json
import requests
from pprint import pprint

import RPi.GPIO as GPIO
import time

from threading import Timer

from mq import *



# init flask application
app = Flask(__name__)

# redis
app.config['REDIS_URL'] = 'redis://localhost'
# sse
# app.register_blueprint(sse, url_prefix='/stream')
app.register_blueprint(sse, url_prefix='/stream2')


# global var
is_on = False
is_leaked = False
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



# -----------------------------------------------------------------------------
# remote GPIO

# uses global variable is_on which states if LED is on or not
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

	return "done"


# set port 18 high
def turn_on():
	print('LED ON')
	GPIO.output(18, GPIO.HIGH)


# let port 18 low
def turn_off():
	print('LED OFF')
	GPIO.output(18, GPIO.LOW)


# turn off and send sse that it was a success
def sse_turn_off():
	global is_on

	turn_off()
	is_on = False


	# need to make sure this exists
	# also, make sure that redis is running on your pi
	with app.app_context():
		# sse, make sure to capture as success in js
		sse.publish({'success': 'True'}, type='success')


# -----------------------------------------------------------------------------
# gas stuff


@app.route('/gas')
def gas():
	print("Press CTRL+C to abort.")

	mq = MQ();
	while True:
		perc = mq.MQPercentage()
		sys.stdout.write("\r")
		sys.stdout.write("\033[K")
		sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
		sys.stdout.flush()
		time.sleep(0.1)

		# if > some level
		# call function
		# sse_leakage_detected()
	# try:
	# 	print("Press CTRL+C to abort.")

	# 	mq = MQ();
	# 	while True:
	# 		perc = mq.MQPercentage()
	# 		sys.stdout.write("\r")
	# 		sys.stdout.write("\033[K")
	# 		sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
	# 		sys.stdout.flush()
	# 		time.sleep(0.1)

	# 		# if > some level
	# 		# call function
	# 		# sse_leakage_detected()

	# except:
	# 	print("\nAbort by user")

	return "success"


def sse_leakage_detected():
	with app.app_context():
		sse2.publish({'leakage': 'True'}, type='leakage')


# -----------------------------------------------------------------------------




# main

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