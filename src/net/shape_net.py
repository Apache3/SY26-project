import lmdb
import numpy as np
import cv2
import caffe
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
import sys

#from picamera.array import PiRGBArray
#from picamera import PiCamera
#import time
 
# initialize the camera and grab a reference to the raw camera capture
def pi_cam_init():
	camera = PiCamera()
	rawCapture = PiRGBArray(camera)
	 
	# allow the camera to warmup
	time.sleep(0.1)
 
# grab an image from the camera
def get_pi_cam_image(camera):
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
	return image
 

def get_cam_image(cam, mirror=False):
  	
	ret_val, img = cam.read()
	if mirror: 
		img = cv2.flip(img, 1)

	h,w,c = img.shape
	border_size = min(w,h)
	#img = img[0:h,(w-h)/2:(w+h)/2]
	return img

def forward_img_to_net(img,net):
	if img.shape != [28,28,3]:
			img2 = cv2.resize(img,(28,28))
			img = img2.reshape(28,28,-1)
	else:
		img = img.reshape(28,28,-1)

	#cv2.imshow('my webcam', img)
	# cv2.waitKey(1) 

	res = net.forward(data = np.asarray([img.transpose(2,0,1)]))
	argmax = res.values()[0]
	pred = res.values()[1]
	print label_tab[pred.argmax()]
	print pred

if len(sys.argv) <2:
	print 'usage: net_test train/predict + img_filename(s)'
	sys.exit(0)

solver_prototxt = 'lenet_solver.prototxt'
predict_prototxt = 'lenet.prototxt'
caffemodel = '_iter_10000.caffemodel'
label_tab = ['Cross', 'Diamond', 'Disc', 'Square', 'Triangle', 'Octogon']

if sys.argv[1] == 'train':
	caffe.set_mode_cpu()
	solver = caffe.get_solver(solver_prototxt)
	solver.solve()

elif sys.argv[1] == 'predict' and len(sys.argv)>2:
	img_filenames=[]
	for i in list(range(len(sys.argv)-2)):
		img_filenames.append(sys.argv[2+i])
		print i

	print img_filenames
	caffe.set_mode_cpu()
	net = caffe.Classifier(predict_prototxt, caffemodel,caffe.TEST,raw_scale=255)
	print "successfully loaded classifier"

	for img_filename in img_filenames:
		
		img = cv2.imread(img_filename)

		if img.shape != [28,28,3]:
			img2 = cv2.resize(img,(28,28))
			img = img2.reshape(28,28,-1)
		else:
			img = img.reshape(28,28,-1)

		res = net.forward(data = np.asarray([img.transpose(2,0,1)]))
		argmax = res.values()[0]
		pred = res.values()[1]
		print label_tab[pred.argmax()]
		print pred
elif sys.argv[1] == 'camera':
	caffe.set_mode_cpu()
	net = caffe.Classifier(predict_prototxt, caffemodel,caffe.TEST,raw_scale=255)
	print "successfully loaded classifier"
	cam = cv2.VideoCapture(0)
	while True:
		img = get_cam_image(cam,True)
		cv2.imshow('my webcam', img)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
		forward_img_to_net(img,net)
		
else:
	print 'usage: net_test train/predict  + img_filename'
	sys.exit(0)