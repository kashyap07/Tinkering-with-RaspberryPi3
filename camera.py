'''
basic camera module
take photo and send to server
'''

from time import sleep
from picamera import PiCamera
import requests


camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

sleep(0.5)
camera.capture('test.jpg')


url = 'http://192.168.0.107:8000/sendphoto'
files = {'image': open('test.jpg', 'rb')}
requests.post(url, files=files)