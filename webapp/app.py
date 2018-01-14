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


if __name__ == '__main__':
	app.run(
		threaded=True,
		debug=True,
		host='0.0.0.0',
		port=8000
	)