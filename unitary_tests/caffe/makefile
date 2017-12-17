train:
	make -C net_test train

test:
	make -C net_test test 
	#python net_test.py predict ../../../database/test/Cross/Cross_0.png
test-all:
	make -C net_test test-all

database:
	make -C lmbd_database generate-database

read-database:
	make -C lmbd_database read-database

clean-state:
	make net_test clean-state

clean-model:
	make net_test clean-model

clean: clean-model clean-state
	