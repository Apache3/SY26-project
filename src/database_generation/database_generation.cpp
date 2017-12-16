//#include "database_generation.h"
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
#include "DatabaseGenerator.h"



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
        DatabaseGenerator dg(original_dir);
        dg.generateDatabase();
    		
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
