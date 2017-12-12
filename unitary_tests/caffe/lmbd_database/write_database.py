import lmdb
import numpy as np
import cv2
import caffe
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
from os import walk

#basic setting
#img size : 128*128*3
#nb img/label : 56
lmdb_file = 'lmdb_data'
batch_size = 256
database_path = '../../../database/'

images_dic ={}
label_dic = {'Cross':0, 'Diamond':1, 'Disc':2, 'Square':3, 'Triangle':4, 'Octogon':5}
for (dirpath, dirnames, filenames) in walk(database_path):
    label = dirpath.split('/')[-1]
    for image_name in filenames :
        images_dic[image_name] = label
    #     print database_path + label + '/' + image_name


# for key in images_dic:
#     print database_path + images_dic[key] + '/' + key
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
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print img.shape
    img = np.transpose(img, (2,0,1))
    #print img.shape
    # cv2.imshow('cv2', img)
    # cv2.waitKey(100)
    #img = caffe.io.load_image(filename)


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