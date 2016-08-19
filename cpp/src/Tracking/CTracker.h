#pragma once
#ifndef _OBJECT
#define _OBJECT
#import "../Candidates/person.hpp"
#endif
#include "TKalmanFilter.h"
#include "HungarianAlg.h"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <vector>
#include <fstream>
using namespace cv;
using namespace std;


class CTracker
{
public:
  CTracker();

  float dist_thres = 90.0;

	size_t maximum_allowed_skipped_frames = 3;
	//
	size_t max_trace_length = 6;

  static size_t NextTrackID;
  size_t minLifetime = 5;
  std::vector<Person> tracks;

	void Update(std::vector<Person> detections, size_t frameNumber, ofstream& csv_file);


	~CTracker();
private:

};
