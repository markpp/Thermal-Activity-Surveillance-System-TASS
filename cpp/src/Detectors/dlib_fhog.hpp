#include <opencv2/opencv.hpp>

#include <dlib/opencv.h>
#include <dlib/svm_threaded.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_processing.h>
#include <dlib/data_io.h>

#include <iostream>
#include <fstream>

#ifndef DEFINES
#define DEFINES
#include "../../defines.hpp"
#endif

#import "../Candidates/person.hpp"
#import "../Detectors/nms.hpp"


using namespace dlib;

class Dlib_fhog {
public:
  Dlib_fhog();
  void train_dlib_detector();
  void load_dlib_detector();

  std::vector<Person> execute_dlib_detector(cv::Mat input_img);


private:
  typedef dlib::scan_fhog_pyramid<dlib::pyramid_down<4> > image_scanner_type;

  void evaluate_dlib_detector(dlib::object_detector<image_scanner_type> &detector, dlib::array<dlib::array2d<unsigned char> > &img_train, dlib::array<dlib::array2d<unsigned char> > &img_test, std::vector<std::vector<dlib::rectangle> > &anno_train,  std::vector<std::vector<dlib::rectangle> > &anno_test);

  cv::Point2i check_coordinate(int x, int y);

  dlib::object_detector<image_scanner_type> mtb_detector;
  dlib::object_detector<image_scanner_type> ped_detector;
};
