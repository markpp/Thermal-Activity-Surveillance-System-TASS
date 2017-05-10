#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>

#include <iostream>
#include <string>
#include <stdio.h>
#include <time.h>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <thread>
#include <iomanip>
#include <fstream>
#include <assert.h>
#include <vector>

using namespace cv;
using namespace std;

//#define video
#define IMAGEWIDTH 80
#define IMAGEHEIGHT 60
int frameNumber = 0;
int startFrameNumber = 0;
int endFrameNumber = 200000;

Mat img;

std::string ZeroPadNumber(int num)
{
    std::ostringstream ss;
    ss << std::setw( 0 ) << std::setfill( '0' ) << num;
    return ss.str();
}

string getParentPath(const string& s) {

   char sep = '/';

   size_t i = s.rfind(sep, s.length());
   if (i != string::npos) {
      return(s.substr(0, i));
   }

   return("");
}

int main( int argc, char** argv )
{
	std::string initialPath = argv[1];
    std::cout << "The initial path is \"" << initialPath << "\"\n";

    while(1) {
        std::string imageFileName = ZeroPadNumber(startFrameNumber) + ".png";
        //std::string imageFileName = "frame_" + ZeroPadNumber(startFrameNumber) + ".png";
	    std::string imageFilePath = initialPath + "/" + imageFileName;
        cout << imageFilePath << std::endl;
	    Mat img = imread(imageFilePath,-1);
	    if (img.empty() || startFrameNumber > endFrameNumber)
		{

		    cout << "the end.." << endl;
			break;
		}    

		flip(img, img, 1);

		std::string newImageFileName = "frame_" + ZeroPadNumber(frameNumber) + ".png";
		std::string imageWritePath = getParentPath(initialPath) + "/" + "fliped/" + newImageFileName;
		//cout << imageWritePath;
		
    	imwrite(imageWritePath, img);

	
	    int k = cv::waitKey(10);
	    if (k=='q') {
	     
	      break;
	    }
	    if(k=='s') {
	      //imwrite("imgBGR.png", imgBGR);
	      //PointCloud.createCompletePointCloud(imgBGR);
	    }
	    if(k=='p') {
	      cv::waitKey();
	    }
	    startFrameNumber++;
	    frameNumber++;
	}
    return 0;
}
