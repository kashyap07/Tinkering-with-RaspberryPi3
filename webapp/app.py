'''
Home Automation System
'''


from flask import Flask, render_template, request, jsonify, abort
import os
import json
import requests
from pprint import pprint


# init flask application
app = Flask(__name__)


# index route
@app.route('/')
def index():
	return render_template('index.html')

# camera page web view
@app.route('/camera')
def camera():
	pass

# raspberry pi casmera route
@app.route('/sendphoto')
def sendphoto():
	data = request.get_json()

	print(data)


if __name__ == '__main__':
	app.run(
		debug=True,
		host=('0.0.0.0'),
		port=8000
	)