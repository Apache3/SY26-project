TEST_IMAGE_CROSS="../../images/Cross/Cross_0.png"
TEST_IMAGE_DIAMOND="../../images/Diamond/Diamond_0.png"
TEST_IMAGE_DISC="../../images/Disc/Disc_0.png"
TEST_IMAGE_SQUARE="../../images/Square/Square_0.png"
TEST_IMAGE_TRIANGLE="../../images/Triangle/triangle_0.png"
TEST_IMAGE_OCTOGON="../../images/Octogon/Octogon_0.png"
TEST_IMAGE_BCKGND="../../images/Background/Backgroung_0.png"

INCLUDE_OCTOGON=False
LEARNIN_ITER=3600

train:
	python shape_net.py train $(INCLUDE_OCTOGON) 

test:
	python shape_net.py predict $(INCLUDE_OCTOGON) $(LEARNIN_ITER) $(TEST_IMAGE_SQUARE)

test-all:
	python shape_net.py predict $(INCLUDE_OCTOGON) $(LEARNIN_ITER) $(TEST_IMAGE_CROSS) $(TEST_IMAGE_DIAMOND) $(TEST_IMAGE_DISC) $(TEST_IMAGE_SQUARE) $(TEST_IMAGE_TRIANGLE) $(TEST_IMAGE_OCTOGON) $(TEST_IMAGE_BCKGND)

shape_net:
	python shape_net.py camera $(INCLUDE_OCTOGON) $(LEARNIN_ITER)
	
train-database:
	python shape_net.py	create_train_db $(INCLUDE_OCTOGON)
test-database:
	python shape_net.py	create_test_db $(INCLUDE_OCTOGON)