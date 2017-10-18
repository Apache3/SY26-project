#include "opencv2/opencv.hpp"
#include <stdlib.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <boost/filesystem.hpp>
#include <boost/filesystem/fstream.hpp> 

#define ANGLE_STEP 15

using namespace boost::filesystem;
using namespace cv;
void modify_image(cv::Mat& img, path p, int max_angle=45, int angle_step = ANGLE_STEP);
Mat rotate(Mat src, double angle);
void add_salt_pepper_Noise(Mat &srcArr, float pa, float pb );
void add_gaussian_Noise(Mat &srcArr,double mean,double sigma);