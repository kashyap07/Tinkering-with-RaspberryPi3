'''
basic camera module
take photo and send to server
'''

from time import sleep
from picamera import PiCamera
import requests
# import RPi.GPIO as GPIO
import time
import datetime
import picamera
import picamera.array
from fractions import Fraction


'''
motion detection part
'''
threshold = 30
sensitivity = 1800

         
def foo():
	print('detected!')
    
       
def check_for_motion(stream1, stream2)
	# h = 128
	# w = 80

	h = 1024
	w = 768

	pix_color = 1	# red=0, green=1, blue=2
	pix_changes = 0

	for w in range(0, w):
		for h in range(0, h):
			diff = abs(int(stream1[h][w][pix_color]) - int(stream2[h][w][pix_color]))
			if diff > threshold:
				pix_changes += 1
			if pix_changes > sensitivity:
				return True
	

def get_stream_img():
	# h = 128
	# w = 80

	h = 1024
	w = 768

	with picamera.PiCamera() as camera:
		time.sleep(0.5)
		camera.resolution = (h, w)
		with picamera.array.PiRGBArray(camera) as stream:
			camera.capture(stream, format='rgb')

			return stream.array


def start_detection():
	# initial stream
	stream1 = get_stream_img()
	while True:
		stream2 = get_stream_img()
		if check_for_motion(stream1, stream2):
			foo()
		stream1 = stream2
	return


'''
capture image and save
'''
def capture_img():
	camera = PiCamera()
	camera.resolution = (1024, 768)
	camera.start_preview()

	sleep(0.5)
	camera.capture('test.jpg')


'''
send captured image
'''
url = 'http://192.168.0.107:8000/sendphoto'
files = {'image': open('test.jpg', 'rb')}
requests.post(url, files=files)