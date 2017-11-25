#include "DatabaseGenerator.h"
#include <opencv2/opencv.hpp>
#include <stdlib.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <boost/filesystem.hpp>
#include <boost/filesystem/fstream.hpp> 
#include <boost/lexical_cast.hpp>
#include <stdio.h>



using namespace cv;
using namespace std;
using namespace boost::filesystem;
using namespace boost;

DatabaseGenerator::DatabaseGenerator(path path_to_images)
{
  m_path_to_images = path_to_images;
}

void DatabaseGenerator::generateDatabase()
{
  Mat origin_image;
  for (directory_iterator itr(m_path_to_images); itr!=directory_iterator(); ++itr)
        {
              path p = itr->path();
              if( is_regular_file(p) )
              {
                origin_image = imread(p.string(),CV_LOAD_IMAGE_COLOR);
                
                string databaseDirName = "database/" + p.stem().string();
                //creating the database folder if it does'nt exists
                path databaseDir = p.parent_path().parent_path()/databaseDirName;
                if ( !exists(databaseDir.parent_path()))
                {
                  create_directory(databaseDir.parent_path());
                }
                //create a folder for the transformed images
                if ( !exists(databaseDir) )
                {
                  create_directory(databaseDir);
                  cout <<"directory created at :"<< canonical(databaseDir) <<endl;
                }

                modify_image(origin_image, databaseDir);

              }
        }
}

//create all the needed transformation of the source image into the path p 
void DatabaseGenerator::modify_image(cv::Mat& img, path p, int max_angle,int angle_step)
{
	string ext = ".png";
	
	for (int angle = 0; angle <= max_angle; angle+=angle_step )
	{
		Mat rot_img = rotate(img,angle);

		string angl_str = lexical_cast<string>(angle);
		string filename = p.string()+"/" + p.stem().string() + "_" + angl_str;

		

		bool res;
		res = imwrite(filename + ext,rot_img);
		if (res)
		{
			cout <<"image written at: "<<filename + ext <<endl;
		}
		else
		{
			cout << "Error while saving " << filename << endl;
		}

		Mat noise_img = rot_img.clone();
		add_salt_pepper_Noise(noise_img, 0.2,0.2);

		res = imwrite(filename + "_snp" + ext,noise_img);
		if (res)
		{
			cout <<"image written at: "<<filename + "_snp" + ext<<endl;
		}
		else
		{
			cout << "Error while saving " << filename << endl;
		}		

		noise_img = rot_img.clone();

		add_gaussian_Noise(noise_img, 0,55);

		res = imwrite(filename + "_gaussian" + ext,noise_img);
		if (res)
		{
			cout <<"image written at: "<<filename + "_gaussian" + ext<<endl;
		}
		else
		{
			cout << "Error while saving " << filename << endl;
		}		

	}
   	
   		
}

//rotates the image aroud its center

Mat DatabaseGenerator::rotate(Mat src, double angle)
{
    Mat dst;
    Point2f pt(src.cols/2., src.rows/2.);    
    Mat r = getRotationMatrix2D(pt, angle, 1.0);
    warpAffine(src, dst, r, Size(src.cols, src.rows));
    return dst;
}

// adds salt and pepper noise. Coded by timlentse (https://github.com/timlentse/Add_Salt-Pepper_Noise), modified a bit
void DatabaseGenerator::add_salt_pepper_Noise(Mat &srcArr, float pa, float pb )

{    RNG rng; 
    int amount1=srcArr.rows*srcArr.cols*pa;
    int amount2=srcArr.rows*srcArr.cols*pb;
    for(int counter=0; counter<amount1; ++counter)
    {
    	srcArr.at<uchar>(rng.uniform(0,srcArr.rows), rng.uniform(0,3*srcArr.cols)) =0;
    }
    
	for (int counter=0; counter<amount2; ++counter)
 	{
		srcArr.at<uchar>(rng.uniform(0,srcArr.rows), rng.uniform(0,3*srcArr.cols)) = 255;
 	}
}

// adds gaussian noise. Coded by timlentse (https://github.com/timlentse/Add_Salt-Pepper_Noise) .
void DatabaseGenerator::add_gaussian_Noise(Mat &srcArr,double mean,double sigma)
{
    Mat NoiseArr = srcArr.clone();
    RNG rng;
    rng.fill(NoiseArr, RNG::NORMAL, mean,sigma);

    add(srcArr, NoiseArr, srcArr);
}