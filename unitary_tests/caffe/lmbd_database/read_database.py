import caffe
import lmdb
import numpy as np
import cv2
import sys
from caffe.proto import caffe_pb2

if len(sys.argv) != 2:
	print 'usage: python read_database.py path_to_database_folder'
	sys.exit(0)
else:
	path = sys.argv[1]

	label_tab = ['Cross', 'Diamond', 'Disc', 'Square', 'Triangle', 'Octogon']
	lmdb_env = lmdb.open(path)
	lmdb_txn = lmdb_env.begin()
	lmdb_cursor = lmdb_txn.cursor()
	datum = caffe_pb2.Datum()

	for key, value in lmdb_cursor:
	    datum.ParseFromString(value)

	    label = datum.label
	    data = caffe.io.datum_to_array(datum)

	    #CxHxW to HxWxC in cv2
	    #print data.shape
	    image = np.transpose(data, (1,2,0))
	    #print  image.shape
	    cv2.imshow('cv2', image)
	    print('{},{}'.format(key, label_tab[label]))
	    cv2.waitKey(300)
	    