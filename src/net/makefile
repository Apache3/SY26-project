TEST_IMAGE_CROSS="../../database/test/Cross/Cross_rot80_con3_bri21_snp3.png"
TEST_IMAGE_DIAMOND="../../database/test/Diamond/Diamond_rot80_con3_bri21_snp3.png"
TEST_IMAGE_DISC="../../database/test/Disc/Disc_rot80_con3_bri21_snp3.png"
TEST_IMAGE_SQUARE="../../database/test/Square/Square_rot80_con3_bri21_snp3.png"
TEST_IMAGE_TRIANGLE="../../database/test/Triangle/Triangle_rot80_con3_bri21_snp3.png"
TEST_IMAGE_OCTOGON="../../database/test/Octogon/Octogon_rot80_con3_bri21_snp3.png"
TEST_IMAGE_BCKGND="../../database/Background.png"


train:
	python shape_net.py train

test:
	python shape_net.py predict $(TEST_IMAGE_SQUARE)

test-all:
	python shape_net.py predict $(TEST_IMAGE_CROSS) $(TEST_IMAGE_DIAMOND) $(TEST_IMAGE_DISC) $(TEST_IMAGE_SQUARE) $(TEST_IMAGE_TRIANGLE) $(TEST_IMAGE_OCTOGON) $(TEST_IMAGE_BCKGND)

camera:
	python shape_net.py camera	
	