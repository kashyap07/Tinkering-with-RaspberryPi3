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


url = '192.168.0.107/sendphoto'
files = {'media': open('test.jpg', 'rb')}
requests.post(url, files=files)