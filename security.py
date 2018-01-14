'''
basic camera module
take photo and send to server
'''

from time import sleep
from picamera import PiCamera
import requests
import RPi.GPIO as GPIO
import time


'''
motion detection part
'''
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN)

try:
	time.sleep(2)
	while True:
		if GPIO.input(23):
			GPIO.output(24, False)
			print("Motion Detected.")
			time.sleep(3)
		time.sleep(0.1)
		
except:
	GPIO.cleanup()


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