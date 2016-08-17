#include <dlib/svm_threaded.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_processing.h>
#include <dlib/data_io.h>

//#include <opencv2/highgui/highgui.hpp>
//#include <opencv2/opencv.hpp>

#include <iostream>
#include <fstream>

using namespace dlib;

class Dlib_fhog {
public:
  Dlib_fhog();
  void train_dlib_detector();
  void load_dlib_detector();

  //void execute_dlib_detector(cv::Mat input_img);


private:
  typedef dlib::scan_fhog_pyramid<dlib::pyramid_down<4> > image_scanner_type;

  //void evaluate_dlib_detector(dlib::object_detector<image_scanner_type> detector, dlib::array<dlib::array2d<unsigned char> > img_train, dlib::array<dlib::array2d<unsigned char> > img_test, std::vector<std::vector<dlib::rectangle> > anno_train,  std::vector<std::vector<dlib::rectangle> > anno_test);
  dlib::object_detector<image_scanner_type> detector;
};
