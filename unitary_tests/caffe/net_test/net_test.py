import lmdb
import numpy as np
import cv2
import caffe
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
import sys

if len(sys.argv) <2 or len(sys.argv) > 3 :
	print 'usage: net_test train/predict + img_filename'
	sys.exit(0)

solver_prototxt = 'lenet_solver.prototxt'
train_test_prototxt = 'lenet_train_test.prototxt'
predict_prototxt = 'lenet.prototxt'
database_folder = '../lmdb_database/lmdb_data/'
caffemodel = '_iter_100.caffemodel'
label_tab = ['Cross', 'Diamond', 'Disc', 'Square', 'Triangle', 'Octogon']

if sys.argv[1] == 'train':
	caffe.set_mode_cpu()
	solver = caffe.get_solver(solver_prototxt)
	solver.solve()

elif sys.argv[1] == 'predict' and len(sys.argv)>2:
	img_filename = sys.argv[2]
	print img_filename
	#img = cv2.imread(img_filename)
	img = caffe.io.load_image(img_filename,color=False)
	caffe.set_mode_cpu()
	net = caffe.Classifier(predict_prototxt, caffemodel,caffe.TEST,raw_scale=255)

	print "successfully loaded classifier"

	# if img.shape != [28,28,3]:
 #    	img2 = cv2.resize(img,(28,28))
 #        img = img2.reshape(28,28,-1)
	# else:
	#     img = img.reshape(28,28,-1)

	img = 1.0 - img/255.0

	res = net.forward(data = np.asarray([img.transpose(2,0,1)]))
	pred = res.values()[0]
	print pred.argmax()
else:
	print 'usage: net_test train/predict  + img_filename'
	sys.exit(0)