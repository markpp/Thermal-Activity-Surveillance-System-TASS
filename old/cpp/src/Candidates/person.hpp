/*--------- INCLUDES------------*/
#include "../Tracking/TKalmanFilter.h"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <vector>

#ifndef DEFINES
#define DEFINES
#include "../../defines.hpp"
#endif

using namespace cv;
using namespace std;

class Person {
public:
  Person(cv::Rect candidate_rect);
  static size_t NextDetectionID;
  vector<Point> trace;
  //static size_t NextDetectionID;
  size_t track_id, detection_id;
  size_t skipped_frames = 0;
  size_t lifetime = 0;
  size_t firstFrame = 0;

  double mtb_score = 0;
  double ped_score = 0;
  double mtb_score_sum = 0;
  double ped_score_sum = 0;
  cv::Point p_detection, p_prediction;
  cv::Rect rect_detection;
  string departureLocation = "inside";
  string type_tag;
  TKalmanFilter* KF;
  bool locateTrack();
  bool classify();
private:

};
