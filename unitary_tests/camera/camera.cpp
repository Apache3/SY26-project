#include "opencv2/opencv.hpp"
#include <raspicam/raspicam.h>
#include <raspicam/raspicam_cv.h>
#include <iostream>
#include <iomanip>
#include <stdlib.h>

using namespace std;
using namespace cv;


int main(int narg, char *argv[]) {
	
    raspicam::RaspiCam_Cv Camera;
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC3);
    //Camera.set ( CV_CAP_PROP_FRAME_WIDTH,  640 );
    //Camera.set ( CV_CAP_PROP_FRAME_HEIGHT, 480);
    Camera.set ( CV_CAP_PROP_BRIGHTNESS,50 );
    Camera.set ( CV_CAP_PROP_CONTRAST ,50);
    Camera.set ( CV_CAP_PROP_SATURATION, 50);
    Camera.set ( CV_CAP_PROP_GAIN, 10 );
    Camera.set ( CV_CAP_PROP_EXPOSURE, 50 );   
    if (!Camera.open()) {
		  cerr<<"Error opening the camera"<<endl;
		  return -1;
	}
    Mat frame;
    cout << "on filme" << endl;
    for(;;) {
		Camera.grab();
        Camera.retrieve ( frame);
        cvtColor(frame,frame,COLOR_BGR2RGB); //oui ou non ???
		imshow("camera", frame);
        if(waitKey(10) >= 0) break;
    }
    Camera.release();
    cout << "that's all folk" << endl;
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}
