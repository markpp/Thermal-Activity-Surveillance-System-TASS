//#include "src/Presentation/Presentation.hpp"
//#include "src/Tools/StringTools.hpp"
#include "src/Tools/FileHandler.hpp"
#include "src/Detectors/dlib_fhog.hpp"
//#include "defines.hpp"

//#include <opencv2/opencv.hpp>
//#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <string>
#include <stdio.h>
#include <time.h>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <thread>
#include <iomanip>

cv::Mat mask12LSB = cv::Mat::zeros(60, 80, CV_16UC1) + 1023; //turninng on the 12 least significant bits, while shutting off the 4 MSB



int outputScale = 8;
int startAtFrame = 0;

cv::Mat read_image(std::string img_path)
{
  cv::Mat depth8U, masked16U;
  cv::Mat img_16 = cv::imread(img_path,-1);
  if (img_16.empty())
    {
      std::cout << "empty image frame.." << std::endl;
      std::cout << "path was: " << img_path << std::endl;
    }
    // apply mask to only use the 12 LSB
    bitwise_and(img_16, mask12LSB, masked16U);
    // remove the 4 LSB and convert to 8bit. Shifting is equivalent to multiplication/division with powers of 2. 6 << 1 = 6*2^1, 6 << 3 = 6*2^3
    masked16U.convertTo(depth8U, CV_8UC1, 1.0/4);
      //imshow("blob",depth8U);
  return depth8U;
}

int main( int argc, char** argv )
{
  cv::namedWindow("Intensity");
  cv::moveWindow("Intensity", -450, -700);

  //Presentation presenter;
  //Counting counter;
  Dlib_fhog dlib_fhog;

  dlib_fhog.train_dlib_detector();

  std::vector<std::vector<std::string> > annotations;

  std::string full_img_path;
  std::string initialPath = argv[1];

  annotations = load_annotations(argv[2]);

  //std::cout << annotations[1][0] << std::endl;
  //while(1)
  //{
  for(auto & anno: annotations) {
    full_img_path = initialPath + "/" + anno[0];
    std::cout << full_img_path << std::endl;
    cv::Mat in_img = read_image(full_img_path);

    //dlib_fhog.execute_dlib_detector(in_img);

    cv::imshow("Intensity", in_img);

    int k = cv::waitKey();
    if (k=='q') {
      //outputVideo.release();
      //myCounter.outputFileStream.close();
      //myCounter.myCTracker.myTrackClassifier.outputFileStream.close();
      break;
    }
    if(k=='n') {

    }
    if(k=='b') {

    }
    if(k=='p') {
      cv::waitKey();
    }
  }
  //pathToFile = getPath2File(initialPath);


  //frameNumber++;
}
