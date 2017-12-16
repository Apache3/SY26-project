#ifndef DATABASE_GENERATOR_H
#define DATABASE_GENERATOR_H

#include <opencv2/opencv.hpp>
#include <stdlib.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <boost/filesystem.hpp>
#include <boost/filesystem/fstream.hpp> 

#define ANGLE_STEP 15

using namespace boost::filesystem;
using namespace cv;

class DatabaseGenerator
{
	public:
		DatabaseGenerator(path path_to_images);
		void generateDatabase(); 

	private:
		path m_path_to_images;
		void modify_image(cv::Mat& img, path p, int max_angle=45, int angle_step = ANGLE_STEP);
		Mat  rotate(Mat src, double angle);
		Mat  contrast(Mat image, double alpha);
		Mat  brightness(Mat image, double beta);
		void add_salt_pepper_Noise(Mat &srcArr, float pa, float pb );
		void add_gaussian_Noise(Mat &srcArr,double mean,double sigma);
		void write_image(Mat img, string filename);
};


#endif