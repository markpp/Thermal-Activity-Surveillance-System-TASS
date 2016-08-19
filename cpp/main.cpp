#include <opencv2/highgui/highgui.hpp>

#include "src/Presentation/presenter.hpp"
#include "src/Tools/StringTools.hpp"
#include "src/Tools/FileHandler.hpp"
#include "src/Detectors/dlib_fhog.hpp"
#include "src/Tracking/CTracker.h"
#include "defines.hpp"

//#include <opencv2/opencv.hpp>
//#include <opencv2/core/core.hpp>

/*
./main /Users/markpp/Desktop/code/my_repos/MTB/data/training/2016-08-08-11-00-training /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/bb/2016-08-08-11-00_bb.csv

./main /Users/markpp/Desktop/code/my_repos/MTB/data/testing/2016-08-09-14-58-testing /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/bb/2016-08-09-14-58_bb.csv

./main /Users/markpp/Desktop/code/data/2016-08-09-14-58-short /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/bb/2016-08-09-14-58_bb.csv

*/
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <time.h>
#include <sstream>
#include <algorithm>
#include <thread>
#include <iomanip>

cv::Mat mask12LSB = cv::Mat::zeros(60, 80, CV_16UC1) + 1023; //turninng on the 12 least significant bits, while shutting off the 4 MSB
cv::Mat output_img;

bool train = false;

int outputScale = 8;
int startAtFrame = 0;

int frameNumber = 0;

/*
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
*/

int main( int argc, char** argv )
{
  cv::namedWindow("Intensity");
  cv::moveWindow("Intensity", -450, -700);

  Presenter presenter;
  Dlib_fhog dlib_fhog;
  CTracker tracker;

  cv::VideoWriter outputVideo; //CV_FOURCC('M','J','P','G')
  outputVideo.open( "/Users/markpp/Desktop/outputVideo.avi", CV_FOURCC('M','J','P','G'), 9, cv::Size (IMAGEWIDTH_SCALE, IMAGEHEIGHT_SCALE), true );

  ofstream myfile;
  myfile.open ("/Users/markpp/Desktop/log.csv");

  cv::Mat in_img;

  if(argv[3]>0)
  {
    train = true;
  }

  if(train)
  {
    dlib_fhog.train_dlib_detector();
  }
  else
  {
    dlib_fhog.load_dlib_detector();

    std::vector<std::vector<std::string> > annotations;
    annotations = load_annotations(argv[2]);

    std::string full_img_path;
    std::string initialPath = argv[1];

    while(1)
    {
    //for(auto & anno: annotations) {
      //frameNumber = getFileNumber(anno[0]);
      //full_img_path = initialPath + "/" + anno[0];

      full_img_path = initialPath + "/" + "frame_" + ZeroPadNumber(frameNumber) + ".png";
      
      cv::Mat depth8U, masked16U;
      cv::Mat img_16 = cv::imread(full_img_path,-1);
      if (img_16.empty())
      {
        std::cout << "empty image frame.." << std::endl;
        std::cout << "path was: " << full_img_path << std::endl;
        break;
      }
      // apply mask to only use the 12 LSB
      bitwise_and(img_16, mask12LSB, masked16U);
      // remove the 4 LSB and convert to 8bit. Shifting is equivalent to multiplication/division with powers of 2. 6 << 1 = 6*2^1, 6 << 3 = 6*2^3
      masked16U.convertTo(in_img, CV_8UC1, 1.0/4);
      //imshow("blob",depth8U);

      cv::resize(in_img, in_img, cv::Size(IMAGEWIDTH_SCALE, IMAGEHEIGHT_SCALE), CV_INTER_LINEAR);

      std::vector<Person> dets = dlib_fhog.execute_dlib_detector(in_img);

      output_img = presenter.draw_frame_number(in_img, frameNumber);

      output_img = presenter.draw_detections(output_img, dets);

      tracker.Update(dets, frameNumber, myfile);
      output_img = presenter.draw_tracks(output_img, tracker.tracks);

      //cv::imshow("Intensity", output_img);
      outputVideo.write(output_img);

      int k = cv::waitKey(10);
      if (k=='q') {
        break;
      }
      if(k=='n') {

      }
      if(k=='b') {

      }
      if(k=='p') {
        cv::waitKey();
      }
      frameNumber++;
    }
    myfile.close();
    outputVideo.release();
  }

  frameNumber++;
}
