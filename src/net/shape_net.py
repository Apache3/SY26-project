import lmdb
import numpy as np
import cv2
import caffe
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
import sys
from os import walk

from picamera.array import PiRGBArray
from picamera import PiCamera

import time
 
# initialize the camera and grab a reference to the raw camera capture
def pi_cam_init():
	camera = PiCamera()
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

def caffe_init():
	caffe.set_mode_cpu()
	net = caffe.Classifier(predict_prototxt, caffemodel,caffe.TEST,raw_scale=1)	 
	return net

def get_cam_image(cam, mirror=False):
  	
	ret_val, img = cam.read()
	if mirror: 
		img = cv2.flip(img, 1)

	h,w,c = img.shape
	border_size = min(w,h)
	#img = img[0:h,(w-h)/2:(w+h)/2]
	return img

def forward_img_to_net(img,net):
	if img.shape != [96,54,3]:
			img2 = cv2.resize(img,(96,54))
			img = img2.reshape(96,54,-1)
	else:
		img = img.reshape(96,54,-1)

	#cv2.imshow('my webcam', img)
	# cv2.waitKey(1) 

	res = net.forward(data = np.asarray([img.transpose(2,0,1)]))
	#res = net.predict(inputs=np.asarray([img.transpose(2,0,1)]))
	argmax = res.values()[0]
	pred = res.values()[1]
	print label_tab[pred.argmax()]
	print pred

def write_database(lmdb_file,batch_size,database_path):

	images_dic ={}
	label_dic = {'Cross':0, 'Diamond':1, 'Disc':2, 'Square':3, 'Triangle':4, 'Octogon':5,'Background':6}
	for (dirpath, dirnames, filenames) in walk(database_path):
	    label = dirpath.split('/')[-1]
	    for image_name in filenames :
	        images_dic[image_name] = label

	# create the lmdb file
	lmdb_env = lmdb.open(lmdb_file, map_size=int(1e12))
	lmdb_txn = lmdb_env.begin(write=True)
	datum = caffe_pb2.Datum()

	item_id = -1
	for key, value in images_dic.items():
	    item_id += 1
	    #prepare the data and label
	    filename = database_path + value +'/' + key
	    

	    img = cv2.imread(filename)
	    img = np.transpose(img, (2,0,1))

	    data = np.asarray(img,dtype=np.uint8)
	    label = label_dic[value]

	    # save in datum
	    datum = caffe.io.array_to_datum(data, label)
	    
	    keystr = '{:0>8d}'.forma
	    t(item_id)
	    lmdb_txn.put( keystr, datum.SerializeToString() )

	    # write batch
	    if(item_id + 1) % batch_size == 0:
	        lmdb_txn.commit()
	        lmdb_txn = lmdb_env.begin(write=True)
	        print (item_id + 1)

	# write last batch
	if (item_id+1) % batch_size != 0:
	    lmdb_txn.commit()
	    print 'last batch'
	    print (item_id + 1)

if len(sys.argv) <2:
	print 'usage: net_test train/predict + img_filename(s)'
	sys.exit(0)

solver_prototxt = 'lenet_solver.prototxt'
predict_prototxt = 'lenet.prototxt'
caffemodel = 'no_bckgnd_iter_3600.caffemodel'
label_tab = ['Cross', 'Diamond', 'Disc', 'Square', 'Triangle', 'Octogon','Background']

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
	net = caffe_init()
	print "successfully loaded classifier"

	for img_filename in img_filenames:
		
		img = cv2.imread(img_filename)
		forward_img_to_net(img,net)

elif sys.argv[1] == 'camera':
	
	caffe.set_mode_cpu()
	net = caffe.Classifier(predict_prototxt, caffemodel,caffe.TEST,raw_scale=1)
	print "successfully loaded classifier"
	#cam = cv2.VideoCapture(0)
	cam, rawCapture = pi_cam_init()
	mean_img = get_pi_cam_image(cam, rawCapture)
	while True:
		#img = get_cam_image(cam,True)
		img = get_pi_cam_image(cam, rawCapture)
		#cv2.imshow('my webcam', img)
		#if cv2.waitKey(1) == 27: 
		#	break  # esc to quit
		forward_img_to_net(img-mean_img,net)

elif sys.argv[1] == 'create_train_db':
	
	lmdb_file = 'shape_train_lmdb/'
	batch_size = 48
	database_path = '../../database/train/'
	write_database(lmdb_file,batch_size,database_path)


elif sys.argv[1] == 'create_test_db':
	lmdb_file = 'shape_test_lmdb/'
	batch_size = 24
	database_path = '../../database/test/'
	write_database(lmdb_file,batch_size,database_path)

else:
	print 'usage: net_test train/predict  + img_filename'
	sys.exit(0)