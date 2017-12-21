import lmdb
import numpy as np
import cv2
# import caffe
import matplotlib.pyplot as plt
import sys
# from os import walk
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def pi_cam_init():
	camera = PiCamera()
	camera.framerate=30
	rawCapture = PiRGBArray(camera)
	 
	# allow the camera to warmup
	time.sleep(0.1)
	return camera,rawCapture
 
# grab an image from the camera
def get_pi_cam_image(camera, rawCapture):
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
	rawCapture.truncate(0)
	return image

cam, rawCapture = pi_cam_init()
# while True:
	
# 	img = get_pi_cam_image(cam, rawCapture)
# 	cv2.imshow('my webcam', img)
# 	if cv2.waitKey(1) == 27: 
# 		break  # esc to quit


for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		#grab the raw NumPy array representing the image - this array
		#will be 3D, representing the width, height and # of channels
		image = frame.array
		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF
		image = cv2.resize(image,(94,56))

		# clear the stream in preparation or the next frame
		rawCapture.truncate(0)

		# Quit if "q" is hit
		if key == ord("q"):
			break