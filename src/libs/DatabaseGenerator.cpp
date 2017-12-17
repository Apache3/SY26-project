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
              path label_path = itr->path();
              if ( is_directory(label_path))
              {
              	for(directory_iterator lbl_itr(label_path); lbl_itr!=directory_iterator();lbl_itr++)
              	{
              		path p = lbl_itr->path();
	              	if( is_regular_file(p) )
					{

						origin_image = imread(p.string(),CV_LOAD_IMAGE_COLOR);
						
						string databaseDirName = "../database/" + label_path.stem().string();
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
						cout << databaseDir << endl;
						modify_image(origin_image, databaseDir,p.stem().string(), 80, 20);//

					}
				}
              }
              //if p is dir

              		//for
              
        }
}

//create all the needed transformation of the source image into the path p 
void DatabaseGenerator::modify_image(cv::Mat& img, path p, string fn, int max_angle,int angle_step)
{
	string ext = ".png";
	
	for (int angle = 0; angle <= max_angle; angle+=angle_step )
	{
		Mat rot_img = rotate(img,angle);
		string angl_str = lexical_cast<string>(angle);
		string filename = p.string()+"/" + fn + "_rot" + angl_str;

		

		//write_image(rot_img, filename + ext);
		

		for (int contrast_value = 1; contrast_value <= 3; contrast_value+=1)
		{
			Mat con_img = contrast(rot_img, contrast_value);
			string con_str = lexical_cast<string>(contrast_value);
			string filename2 = filename + "_con" + con_str;


			for (int brightness_value = 1; brightness_value <= 10; brightness_value+=3)
			{
				Mat bri_img = brightness(con_img, brightness_value);
				string bri_str = lexical_cast<string>(brightness_value);
				string filename3 = filename2 + "_bri" + bri_str;

				write_image(bri_img, filename3 + ext);

				Mat noise_img;
				stringstream convert;
				
				// for(int i = 1; i <= 6; i=i+2)
				// {
				// 	noise_img = bri_img.clone();
				// 	add_salt_pepper_Noise(noise_img, 0.05*i,0.05*i);
				// 	convert << i;
				// 	write_image(noise_img, filename3 + "_snp"+ convert.str() + ext);
				// 	convert.str("");
				// }
				
				for(int i = 1; i <= 8; i=i+2)
				{
					noise_img = bri_img.clone();
					add_gaussian_Noise(noise_img, 0,10*i);
					convert << i;
					write_image(noise_img, filename3 + "_gau" + convert.str() + ext);
					convert.str("");
				}
			}
		}
			

	}
   	
   		
}

//rotates the image aroud its center

Mat DatabaseGenerator::contrast(Mat image, double alpha) //plz alpha between 1.0 and 3.0
{
	Mat new_image = Mat::zeros(image.size(), image.type());
		for( int y = 0; y < image.rows; y++ )
    	{ 
    		for( int x = 0; x < image.cols; x++ )
    		{
    			for( int c = 0; c < 3; c++ )
    			{
    				new_image.at<Vec3b>(y,x)[c] = saturate_cast<uchar>( alpha*( image.at<Vec3b>(y,x)[c] ));
    			}
 		   	}
		}
	return new_image;
}

Mat DatabaseGenerator::brightness(Mat image, double beta) //plz beta between 1 and 100
{
	Mat new_image = Mat::zeros(image.size(), image.type());
		for( int y = 0; y < image.rows; y++ )
    	{ 
    		for( int x = 0; x < image.cols; x++ )
    		{
    			for( int c = 0; c < 3; c++ )
    			{
    				new_image.at<Vec3b>(y,x)[c] = saturate_cast<uchar>(( image.at<Vec3b>(y,x)[c] + beta));
    			}
 		   	}
		}
	return new_image;
}

Mat DatabaseGenerator::rotate(Mat src, double angle)
{
    Mat dst;
    Point2f pt(src.cols/2., src.rows/2.);    
    Mat r = getRotationMatrix2D(pt, angle, 1.0);
    warpAffine(src, dst, r, Size(src.cols, src.rows));
    return dst;
}

void DatabaseGenerator::write_image(Mat img, string filename)
{
	bool res = imwrite(filename,img);
	if (res)
	{
		cout <<"image written at: "<< filename <<endl;
	}
	else
	{
		cout << "Error while saving " << filename << endl;
	}	
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