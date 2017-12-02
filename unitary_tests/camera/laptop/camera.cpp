// #include <stdio.h>
// #include <opencv2/opencv.hpp>
// #include <opencv2/highgui/highgui.hpp>


// typedef IplImage* (*callback_prototype)(IplImage*);


// /* 
//  * make_it_gray: custom callback to convert a colored frame to its grayscale version.
//  * Remember that you must deallocate the returned IplImage* yourself after calling this function.
//  */
// IplImage* make_it_gray(IplImage* frame)
// {
//     // Allocate space for a new image
//     IplImage* gray_frame = 0;
//     gray_frame = cvCreateImage(cvSize(frame->width, frame->height), frame->depth, 1);
//     if (!gray_frame)
//     {
//       fprintf(stderr, "!!! cvCreateImage failed!\n" );
//       return NULL;
//     }

//     cvCvtColor(frame, gray_frame, CV_RGB2GRAY);
//     return gray_frame; 
// }

// /*
//  * process_video: retrieves frames from camera and executes a callback to do individual frame processing.
//  * Keep in mind that if your callback takes too much time to execute, you might loose a few frames from 
//  * the camera.
//  */
// void process_video()
// {           
//     // Initialize camera
//     CvCapture *capture = 0;
//     capture = cvCaptureFromCAM(-1);
//     if (!capture) 
//     {
//       fprintf(stderr, "!!! Cannot open initialize webcam!\n" );
//       return;
//     }

//     // Create a window for the video 
//     cvNamedWindow("result", CV_WINDOW_AUTOSIZE);

//     IplImage* frame = 0;
//     char key = 0;
//     while (key != 27) // ESC
//     {    
//       frame = cvQueryFrame(capture);
//       if(!frame) 
//       {
//           fprintf( stderr, "!!! cvQueryFrame failed!\n" );
//           break;
//       }

//       // Execute callback on each frame
//       //IplImage* processed_frame = (*custom_cb)(frame);

//       // Display processed frame
//       //cvShowImage("result", processed_frame);
//       cvShowImage("result", frame);

//       // Release resources
//       //cvReleaseImage(&processed_frame);
//       cvReleaseImage(&frame);

//       // Exit when user press ESC
//       key = cvWaitKey(10);
//     }

//     // Free memory
//     cvDestroyWindow("result");
//     cvReleaseCapture(&capture);
// }

// int main( int argc, char **argv )
// {
//     process_video();

//     return 0;
// }

#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{
    VideoCapture cap(0); // open the video camera no. 0

    if (!cap.isOpened())  // if not success, exit program
    {
        cout << "Cannot open the video cam" << endl;
        return -1;
    }

   double dWidth = cap.get(CV_CAP_PROP_FRAME_WIDTH); //get the width of frames of the video
   double dHeight = cap.get(CV_CAP_PROP_FRAME_HEIGHT); //get the height of frames of the video

    cout << "Frame size : " << dWidth << " x " << dHeight << endl;

    namedWindow("MyVideo",CV_WINDOW_AUTOSIZE); //create a window called "MyVideo"

    while (1)
    {
        Mat frame;

        bool bSuccess = cap.read(frame); // read a new frame from video

        if (!bSuccess) //if not success, break loop
        {
             cout << "Cannot read a frame from video stream" << endl;
             break;
        }

        imshow("MyVideo", frame); //show the frame in "MyVideo" window

        if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
       {
            cout << "esc key is pressed by user" << endl;
            break; 
       }
    }
    return 0;

}