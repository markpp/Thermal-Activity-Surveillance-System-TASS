#import "dlib_fhog.hpp"

Dlib_fhog::Dlib_fhog()
{

}

void Dlib_fhog::train_dlib_detector()
{
  dlib::array<dlib::array2d<unsigned char> > mtb_img_train, mtb_img_test, ped_img_train, ped_img_test;
  std::vector<std::vector<dlib::rectangle> > mtb_anno_train, mtb_anno_test, ped_anno_train, ped_anno_test;

  load_image_dataset(mtb_img_train, mtb_anno_train, "../../data/training/training_mtb.xml");
  load_image_dataset(mtb_img_test, mtb_anno_test, "../../data/testing/testing_mtb.xml");
  load_image_dataset(ped_img_train, ped_anno_train, "../../data/training/training_ped.xml");
  load_image_dataset(ped_img_test, ped_anno_test, "../../data/testing/testing_ped.xml");

  // Now we do a little bit of pre-processing.  This is optional but for
  // this training data it improves the results.  The first thing we do is
  // increase the size of the images by a factor of two.  We do this
  // because it will allow us to detect smaller faces than otherwise would
  // be practical (since the faces are all now twice as big).  Note that,
  // in addition to resizing the images, these functions also make the
  // appropriate adjustments to the face boxes so that they still fall on
  // top of the faces after the images are resized.
  dlib::upsample_image_dataset<dlib::pyramid_down<2> >(mtb_img_train, mtb_anno_train);
  dlib::upsample_image_dataset<dlib::pyramid_down<2> >(mtb_img_test,  mtb_anno_test);
  dlib::upsample_image_dataset<dlib::pyramid_down<2> >(ped_img_train, ped_anno_train);
  dlib::upsample_image_dataset<dlib::pyramid_down<2> >(ped_img_test,  ped_anno_test);
  // Since human faces are generally left-right symmetric we can increase
  // our training dataset by adding mirrored versions of each image back
  // into img_train.  So this next step doubles the size of our
  // training dataset.  Again, this is obviously optional but is useful in
  // many object detection tasks.
  add_image_left_right_flips(mtb_img_train, mtb_anno_train);
  add_image_left_right_flips(ped_img_train, ped_anno_train);
  std::cout << "MTB training images: " << mtb_img_train.size() << "MTB testing images: " << mtb_img_test.size() << std::endl;
  std::cout << "PED training images: " << ped_img_train.size() << "PED testing images: " << ped_img_test.size() << std::endl;
  // Finally we get to the training code.  dlib contains a number of
  // object detectors.  This typedef tells it that you want to use the one
  // based on Felzenszwalb's version of the Histogram of Oriented
  // Gradients (commonly called HOG) detector.  The 6 means that you want
  // it to use an image pyramid that downsamples the image at a ratio of
  // 5/6.  Recall that HOG detectors work by creating an image pyramid and
  // then running the detector over each pyramid level in a sliding window
  // fashion.
  image_scanner_type mtb_scanner, ped_scanner;
  // The sliding window detector will be 80 pixels wide and 80 pixels tall.
  // This means that the detector can only output detections that are at least
  // 80 by 80 pixels in size
  mtb_scanner.set_detection_window_size(60, 70);
  ped_scanner.set_detection_window_size(50, 100);
  dlib::structural_object_detection_trainer<image_scanner_type> mtb_trainer(mtb_scanner);
  dlib::structural_object_detection_trainer<image_scanner_type> ped_trainer(ped_scanner);
  // Set this to the number of processing cores on your machine.
  mtb_trainer.set_num_threads(4);
  ped_trainer.set_num_threads(4);
  // The trainer is a kind of support vector machine and therefore has the usual SVM
  // C parameter.  In general, a bigger C encourages it to fit the training data
  // better but might lead to overfitting.  You must find the best C value
  // empirically by checking how well the trained detector works on a test set of
  // images you haven't trained on.  Don't just leave the value set at 1.  Try a few
  // different C values and see what works best for your data.
  mtb_trainer.set_c(4);
  ped_trainer.set_c(4);
  // We can tell the trainer to print it's progress to the console if we want.
  mtb_trainer.be_verbose();
  ped_trainer.be_verbose();
  // The trainer will run until the "risk gap" is less than 0.01.  Smaller values
  // make the trainer solve the SVM optimization problem more accurately but will
  // take longer to train.  For most problems a value in the range of 0.1 to 0.01 is
  // plenty accurate.  Also, when in verbose mode the risk gap is printed on each
  // iteration so you can see how close it is to finishing the training.
  mtb_trainer.set_epsilon(0.02);
  ped_trainer.set_epsilon(0.01);

  // Now we run the trainer.  For this example, it should take on the order of 10
  // seconds to train.
  dlib::object_detector<image_scanner_type> mtb_detector = mtb_trainer.train(mtb_img_train, mtb_anno_train);

  dlib::object_detector<image_scanner_type> ped_detector = ped_trainer.train(ped_img_train, ped_anno_train);

  // You can see how many separable filters are inside your detector like so:
  cout << "Number of MTB filters: "<< num_separable_filters(mtb_detector) << endl;
  cout << "Number of PED filters: "<< num_separable_filters(ped_detector) << endl;

  // Like everything in dlib, you can save your detector to disk using the
  // serialize() function.
  dlib::serialize("../../data/models/detector_mtb.svm") << mtb_detector;
  dlib::serialize("../../data/models/detector_ped.svm") << ped_detector;

  std::cout << "Evaluating MTB detector: " << std::endl;
  evaluate_dlib_detector(mtb_detector, mtb_img_train, mtb_img_test, mtb_anno_train, mtb_anno_test);
  std::cout << "Evaluating PED detector: " << std::endl;
  evaluate_dlib_detector(ped_detector, ped_img_train, ped_img_test, ped_anno_train, ped_anno_test);

  // If you have read any papers that use HOG you have probably seen the nice looking
  // "sticks" visualization of a learned HOG detector.  This next line creates a
  // window with such a visualization of our detector.  It should look somewhat like
  // a face.
  //image_window mtb_hogwin(draw_fhog(mtb_detector), "Learned mtb fHOG detector");
  //image_window ped_hogwin(draw_fhog(ped_detector), "Learned ped fHOG detector");
}

void Dlib_fhog::load_dlib_detector()
{
  // Then you can recall it using the deserialize() function.
  dlib::deserialize("../../data/models/detector_mtb.svm") >> mtb_detector;
  dlib::deserialize("../../data/models/detector_ped.svm") >> ped_detector;
}


void Dlib_fhog::evaluate_dlib_detector(dlib::object_detector<image_scanner_type> &detector, dlib::array<dlib::array2d<unsigned char> > &img_train, dlib::array<dlib::array2d<unsigned char> > &img_test, std::vector<std::vector<dlib::rectangle> > &anno_train,  std::vector<std::vector<dlib::rectangle> > &anno_test)
{

  // Now that we have a face detector we can test it.  The first statement tests it
  // on the training data.  It will print the precision, recall, and then average precision.
  std::cout << "training results: " << dlib::test_object_detection_function(detector, img_train, anno_train) << std::endl;
  // However, to get an idea if it really worked without overfitting we need to run
  // it on images it wasn't trained on.  The next line does this.  Happily, we see
  // that the object detector works perfectly on the testing images.
  std::cout << "testing results:  " << dlib::test_object_detection_function(detector, img_test, anno_test) << std::endl;

}


std::vector<Person> Dlib_fhog::execute_dlib_detector(cv::Mat input_img)
{
  dlib::cv_image<unsigned char> cimg(input_img);
  //std::vector<dlib::rectangle> rectangles = mtb_detector(cimg);


  std::vector<std::pair<double, dlib::rectangle> > mtb_dets;
  mtb_detector(cimg, mtb_dets);

  std::vector<std::pair<double, dlib::rectangle> > ped_dets;
  ped_detector(cimg, ped_dets);

  //std::vector<object_detector<image_scanner_type> > my_detectors;
  //my_detectors.push_back(detector);
  //std::vector<rectangle> dets = evaluate_detectors(my_detectors, images_train[0]);

  std::vector<std::pair<double, dlib::rectangle> > final_mtb_dets;
  std::vector<std::pair<double, dlib::rectangle> > final_ped_dets;

  /*
  int overlap_counter = 5;
  while(overlap_counter != 0)
  {
    if(mtb_dets.size()>0 && ped_dets.size()>0)
    {
      for(auto & mtb_det: mtb_dets)
      {
        for(auto & ped_det: ped_dets)
        {
          if(mtb_det.second.left() < ped_det.second.right() &&
             mtb_det.second.right() > ped_det.second.left() &&
             mtb_det.second.top() < ped_det.second.bottom() &&
             mtb_det.second.bottom() > ped_det.second.top() )
          {
            // overlap
            std::cout << "overlap" << std::endl;
            if(mtb_det.first >= ped_det.first)
            {
              final_mtb_dets.push_back(mtb_det);
            }
            else
            {
              final_ped_dets.push_back(ped_det);
            }
          }
          else
          {
            // no overlap
            final_mtb_dets.push_back(mtb_det);
            final_ped_dets.push_back(ped_det);
          }
        }
      }
    }
    else
    {
      for(auto & mtb_det: mtb_dets)
      {
        final_mtb_dets.push_back(mtb_det);
      }
      for(auto & ped_det: ped_dets)
      {

        final_ped_dets.push_back(ped_det);
      }
    }
    mtb_dets = final_mtb_dets;
    ped_dets = final_ped_dets;
  }
*/


  std::vector<Person> persons;
  for(auto & mtb_det: mtb_dets)
  {
    //cv::Rect bounding_box = cv::Rect(rect.left(), rect.top(), rect.right()-rect.left(), rect.top()-rect.bottom());
    cv::Rect bounding_box = cv::Rect(check_coordinate(mtb_det.second.left(), mtb_det.second.top()), check_coordinate(mtb_det.second.right(), mtb_det.second.bottom()));

    //std::cout << bounding_box  << std::endl;
    Person new_person = Person(bounding_box);
    new_person.mtb_score = mtb_det.first;
    persons.push_back(new_person);
  }

  for(auto & ped_det: ped_dets)
  {
    //cv::Rect bounding_box = cv::Rect(rect.left(), rect.top(), rect.right()-rect.left(), rect.top()-rect.bottom());
    cv::Rect bounding_box = cv::Rect(check_coordinate(ped_det.second.left(), ped_det.second.top()), check_coordinate(ped_det.second.right(), ped_det.second.bottom()));

    //std::cout << bounding_box  << std::endl;
    Person new_person = Person(bounding_box);
    new_person.ped_score = ped_det.first;
    persons.push_back(new_person);
  }

  std::vector<Person> final_persons;

  if(persons.size()>0)
  {
    for(size_t i=0;i<persons.size();i++)
    {
      bool keep = true;
      for(size_t j=0;j<persons.size();j++)
      {
        if(j!=i)
        {
          if(persons[i].rect_detection.x < persons[j].rect_detection.x+persons[j].rect_detection.width &&
             persons[i].rect_detection.x+persons[i].rect_detection.width > persons[j].rect_detection.x &&
             persons[i].rect_detection.y < persons[j].rect_detection.y+persons[j].rect_detection.height  &&
             persons[i].rect_detection.y+persons[i].rect_detection.height > persons[j].rect_detection.y )
          {
            // overlap
            if(!(persons[i].mtb_score >= persons[j].mtb_score && persons[i].mtb_score >= persons[j].ped_score) ||
               !(persons[i].ped_score >= persons[j].mtb_score && persons[i].ped_score >= persons[j].ped_score))
            {
              keep = false;
            }
          }
        }
      }
      if(keep)
      {
        final_persons.push_back(persons[i]);
      }
    }
  }


  //*/
  return final_persons;
}

cv::Point2i Dlib_fhog::check_coordinate(int x, int y)
{
  if(x < 0)
  {
    x = 0;
  }
  if(x >= IMAGEWIDTH_SCALE-1)
  {
    x = IMAGEWIDTH_SCALE-1;
  }
  if(y < 0)
  {
    y = 0;
  }
  if(y >= IMAGEHEIGHT_SCALE-1)
  {
    y = IMAGEHEIGHT_SCALE-1;
  }

  return cv::Point2i(x, y);
}
