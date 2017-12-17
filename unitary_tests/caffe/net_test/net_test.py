import lmdb
import numpy as np
import cv2
import caffe
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
import sys

if len(sys.argv) <2:
	print 'usage: net_test train/predict + img_filename(s)'
	sys.exit(0)

solver_prototxt = 'lenet_solver.prototxt'
predict_prototxt = 'lenet.prototxt'
caffemodel = '_iter_5000.caffemodel'
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
		

		#img = caffe.io.load_image(img_filename,color=False)
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
		#print label_tab[int(argmax)]
		print pred

else:
	print 'usage: net_test train/predict  + img_filename'
	sys.exit(0)