import lmdb
import numpy as np
import cv2
import caffe
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
import sys
from os import walk

#from picamera.array import PiRGBArray
#from picamera import PiCamera

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
#initialize a net
def caffe_init():
	caffe.set_mode_cpu()
	learn_iter = sys.argv[3]
	#choosing between learning with or without octogon
	if include_octogon == 'True':
		caffemodel = 'octogon_learning/shapenet_oct_iter_'+learn_iter+'.caffemodel'
	elif include_octogon =='False':
		caffemodel = 'no_octogon_learning/shapenet_no_oct_iter_'+learn_iter+'.caffemodel'
	else:
		print('ERROR: wrong input for include_octogon')

	net = caffe.Classifier(predict_prototxt, caffemodel,caffe.TEST,raw_scale=1)	 
	print "successfully loaded classifier"
	return net

#get image from webcam
def get_cam_image(cam, mirror=False):
  	
	ret_val, img = cam.read()
	if mirror: 
		img = cv2.flip(img, 1)

	h,w,c = img.shape
	border_size = min(w,h)
	#img = img[0:h,(w-h)/2:(w+h)/2]
	return img
#gives an image to the net for classification
def forward_img_to_net(img,net):
	#image reshape
	if img.shape != [96,54,3]:
			img2 = cv2.resize(img,(96,54))
			img = img2.reshape(96,54,-1)
	else:
		img = img.reshape(96,54,-1)

	#cv2.imshow('my webcam', img)
	# cv2.waitKey(1) 

	#computes predictions
	res = net.forward(data = np.asarray([img.transpose(2,0,1)]))
	#res = net.predict(inputs=np.asarray([img.transpose(2,0,1)]))
	argmax = res.values()[0]
	pred = res.values()[1]
	print label_tab[pred.argmax()]
	print pred

#write an lmdb database from images
def write_database(lmdb_file,batch_size,database_path,include_octogon):

	images_dic ={}

	for (dirpath, dirnames, filenames) in walk(database_path):
	    label = dirpath.split('/')[-1]
	    for image_name in filenames :

	    	#octogon images exclusion
	    	if include_octogon or (not 'Octogon' in image_name):  
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
	    
	    keystr = '{:0>8d}'.format(item_id)
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

if len(sys.argv) <3:
	print('usage: net_test train include_octogon(0 or 1)')
	print('usage: net_test test include_octogon(0 or 1) filename')
	print('usage: net_test camera include_octogon(0 or 1)')
	print('usage: net_test create_train_db include_octogon(0 or 1)')
	print('usage: net_test create_train_db include_octogon(0 or 1)')
	sys.exit(0)

include_octogon = sys.argv[2]
#setting filenames
if include_octogon == 'True':
	solver_prototxt = 'shapenet_solver_oct.prototxt'
	predict_prototxt = 'shapenet_oct.prototxt'	
elif include_octogon == 'False':
	solver_prototxt = 'shapenet_solver_no_oct.prototxt'
	predict_prototxt = 'shapenet_no_oct.prototxt'	
else:
	print('ERROR: wrong input for include_octogon')


#definitions of labels
label_tab = ['Cross', 'Diamond', 'Disc', 'Square', 'Triangle', 'Octogon']
label_dic = {'Cross':0, 'Diamond':1, 'Disc':2, 'Square':3, 'Triangle':4, 'Octogon':5}

if sys.argv[1] == 'train':
	#trains the network
	caffe.set_mode_cpu()
	solver = caffe.get_solver(solver_prototxt)
	solver.solve()

elif sys.argv[1] == 'predict' and len(sys.argv)>3:
	#predictions with input images, as a test
	img_filenames=[]

	for i in list(range(len(sys.argv)-4)):
		img_filenames.append(sys.argv[4+i])
		print i

	print img_filenames
	net = caffe_init()
	print "successfully loaded classifier"

	for img_filename in img_filenames:
		
		img = cv2.imread(img_filename)
		forward_img_to_net(img,net)

elif sys.argv[1] == 'camera':
	
	
	net = caffe_init()
	
	#cam = cv2.VideoCapture(0)
	#initialize camera
	cam, rawCapture = pi_cam_init()
	while True:
		#img = get_cam_image(cam,True)
		img = get_pi_cam_image(cam, rawCapture)
		#cv2.imshow('my webcam', img)
		#if cv2.waitKey(1) == 27: 
		#	break  # esc to quit
		forward_img_to_net(img,net)

elif sys.argv[1] == 'create_train_db':
	
	
	if include_octogon == 'True':
		lmdb_file = 'shape_train_oct_lmdb/'
		batch_size = 60
		inc_oct=True
	elif include_octogon == 'False':
		lmdb_file = 'shape_train_no_oct_lmdb/'
		batch_size = 60
		inc_oct=False
	else:
		print('ERROR: wrong input for include_octogon')

	database_path = '../../database/train/'
	write_database(lmdb_file,batch_size,database_path,inc_oct)


elif sys.argv[1] == 'create_test_db':
	
	if include_octogon == 'True':
		lmdb_file = 'shape_test_oct_lmdb/'
		batch_size = 36
		inc_oct = True
	elif include_octogon == 'False':
		lmdb_file = 'shape_test_no_oct_lmdb/'
		batch_size = 60
		inc_oct = False
	else:
		print('ERROR: wrong input for include_octogon')
	
	database_path = '../../database/test/'
	write_database(lmdb_file,batch_size,database_path,inc_oct)

else:
	print('usage: net_test train include_octogon(0 or 1)')
	print('usage: net_test test include_octogon(0 or 1) filename')
	print('usage: net_test camera include_octogon(0 or 1)')
	print('usage: net_test create_train_db include_octogon(0 or 1)')
	print('usage: net_test create_train_db include_octogon(0 or 1)')
	sys.exit(0)