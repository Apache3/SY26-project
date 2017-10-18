#include "database_generation.h"
#include "opencv2/opencv.hpp"
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

int main( int argc, char** argv )
{
    if ( argc != 2)
    {
     cout <<" Usage: ./database_generation image_to_transform_folder " << endl;
     return -1;
    }

    path original_dir(argv[1]);
    Mat origin_image;
    Mat trans_image;

    if ( exists(original_dir) )
    {
    	
    	if (is_directory(original_dir) )
    	{

    		for (directory_iterator itr(original_dir); itr!=directory_iterator(); ++itr)
    		{
          		path p = itr->path();
          		if( is_regular_file(p) )
          		{
          			origin_image = imread(p.string(),CV_LOAD_IMAGE_COLOR);
	          		
          			string dirname = "database/" + p.stem().string();
					//creating the database folder if it does'nt exists
      				path newdir = p.parent_path().parent_path()/dirname;
          			if ( !exists(newdir.parent_path()))
          			{
          				create_directory(newdir.parent_path());
          			}
          			//create a folder for the transformed images
          			if ( !exists(newdir) )
	          		{
	          			create_directory(newdir);
	          			cout <<"directory created at :"<< canonical(newdir) <<endl;
	          		}

	          		modify_image(origin_image, newdir);

          		}
    		}
    	}
    	else
    	{
    		cout << "argument 1 must be a directory!" << endl;
    		cout << "exiting..." << endl;
    	}
    }
    else
    {
    	cout << "the path doesn't exist" << endl;
    	cout << "exiting..." << endl;
    }

    return 0;
}

//create all the needed transformation of the source image into the path p 
void modify_image(cv::Mat& img, path p, int max_angle,int angle_step)
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

Mat rotate(Mat src, double angle)
{
    Mat dst;
    Point2f pt(src.cols/2., src.rows/2.);    
    Mat r = getRotationMatrix2D(pt, angle, 1.0);
    warpAffine(src, dst, r, Size(src.cols, src.rows));
    return dst;
}

// adds salt and pepper noise. Coded by timlentse (https://github.com/timlentse/Add_Salt-Pepper_Noise), modified a bit
void add_salt_pepper_Noise(Mat &srcArr, float pa, float pb )

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
void add_gaussian_Noise(Mat &srcArr,double mean,double sigma)
{
    Mat NoiseArr = srcArr.clone();
    RNG rng;
    rng.fill(NoiseArr, RNG::NORMAL, mean,sigma);

    add(srcArr, NoiseArr, srcArr);
}