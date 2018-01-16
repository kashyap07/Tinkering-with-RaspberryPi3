'''
basic camera module
take photo and send to server
'''

from time import sleep
from picamera import PiCamera
import requests
import RPi.GPIO as GPIO


'''
motion detection part
'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

try:
	sleep(2)
	while True:
		print(GPIO)
		if GPIO.input(4):
			print('yay')
			sleep(3)
		sleep(0.1)
		
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