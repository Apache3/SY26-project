from picamera.array import PiRGBArray
from picamera import PiCamera
 
import time
import sys
import cv2
import os

def pi_cam_init():
	camera = PiCamera()
	rawCapture = PiRGBArray(camera)
	 
	# allow the camera to warmup
	time.sleep(0.1)
	return camera,rawCapture
 
# grab an image from the camera
def get_pi_cam_image(camera, rawCapture):
	camera.capture(rawCapture, format='bgr')
	image = rawCapture.array
	rawCapture.truncate(0)
	return image


def get_cam_image(cam, mirror=False):
  	
	ret_val, img = cam.read()
	if mirror: 
		img = cv2.flip(img, 1)

	h,w,c = img.shape
	border_size = min(w,h)
	#img = img[0:h,(w-h)/2:(w+h)/2]
	return img
def display_help():
	print('c for Cross')
	print('d for Disc')
	print('l for Diamond (losange)')
	print('s for Square')
	print('t for Triangle')
	print('o for Octogon')
	print('b for Background')
	print('clean to clean all')
	print('x to exit')

def check_directory(dir_path):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
		print('Directory created at '+dir_path)

def save_shape(img, images_path, nbr, img_name,img_counter):
	check_directory(images_path+img_name)
	filename = images_path + img_name + '/' 
	filename = filename + img_name+'_'+ str(img_counter[nbr]) +'.png'
	while os.path.exists(filename):
		img_counter[nbr]+=1
		filename = images_path + img_name + '/' 
		filename = filename + img_name+'_'+ str(img_counter[nbr]) +'.png'

	cv2.imwrite(filename,img)
	print('image saved at ' + filename)
	cv2.imshow('lolilol',img)
	cv2.waitKey(1)
	return img_counter

images_path='../../images/'

#cam = cv2.VideoCapture(0)
cam, rawCapture = pi_cam_init()

display_help()
img_counter=[0,0,0,0,0,0,0]
img_size = (96,54)
names=['Cross','Disc', 'Diamond', 'Square', 'Triangle','Octogon','Background']
check_directory(images_path)
while True:
	#img = get_pi_cam_image(cam,rawCapture)
	
	cmd = raw_input('\n')
	#img = get_cam_image(cam,True)
	img = get_pi_cam_image(cam, rawCapture)
	img = cv2.resize(img,img_size)
	if cmd == 'c':
		img_counter = save_shape(img, images_path, 0,names[0], img_counter)

	elif cmd == 'd':
		img_counter = save_shape(img, images_path, 1,names[1], img_counter)
	elif cmd == 'l':
		img_counter = save_shape(img, images_path, 2,names[2], img_counter)
	elif cmd == 's':
		img_counter = save_shape(img, images_path, 3,names[3], img_counter)
	elif cmd == 't':
		img_counter = save_shape(img, images_path, 4,names[4], img_counter)
	elif cmd == 'o':
		img_counter = save_shape(img, images_path, 5,names[5], img_counter)
	elif cmd == 'b':
		img_counter = save_shape(img, images_path, 6,names[6], img_counter)
	elif cmd == 'clean':
		print('cleaning files...')	
		for dir_name in names:
			if os.path.exists(images_path+dir_name):
				for file in os.listdir(dir_name):

					print(images_path + dir_name + file) 
					os.remove(images_path + dir_name + '/' + file)
				print('Directory ' + dir_name +' cleaned.' )
	elif cmd == 'x':
		break;
	else:
		display_help()
