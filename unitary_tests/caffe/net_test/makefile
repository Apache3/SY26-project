TEST_IMAGE_CROSS="../../../database/test/Cross/Cross_0.png"
TEST_IMAGE_DIAMOND="../../../database/test/Diamond/Diamond_0.png"
TEST_IMAGE_DISC="../../../database/test/Disc/Disc_0.png"
TEST_IMAGE_SQUARE="../../../database/test/Square/Square_0.png"
TEST_IMAGE_TRIANGLE="../../../database/test/Triangle/Triangle_0.png"
TEST_IMAGE_OCTOGON="../../../database/test/Octogon/Octogon_0.png"


train:
	python net_test.py train

test:
	python net_test.py predict $(TEST_IMAGE_SQUARE)

test-all:
	python net_test.py predict $(TEST_IMAGE_CROSS) $(TEST_IMAGE_DIAMOND) $(TEST_IMAGE_DISC) $(TEST_IMAGE_SQUARE) $(TEST_IMAGE_TRIANGLE) $(TEST_IMAGE_OCTOGON)

clean-state:
	rm *.solverstate

clean-model:
	rm *.caffemodel

clean: clean-model clean-state
	