#import "dlib_fhog.hpp"

Dlib_fhog::Dlib_fhog()
{

}

void Dlib_fhog::train_dlib_detector()
{
  dlib::array<dlib::array2d<unsigned char> > img_train, img_test;
  std::vector<std::vector<dlib::rectangle> > anno_train, anno_test;

  load_image_dataset(img_train, anno_train, "../../data/training/training_mtb.xml");
  load_image_dataset(img_test, anno_test, "../../data/testing/testing_mtb.xml");

  // Now we do a little bit of pre-processing.  This is optional but for
  // this training data it improves the results.  The first thing we do is
  // increase the size of the images by a factor of two.  We do this
  // because it will allow us to detect smaller faces than otherwise would
  // be practical (since the faces are all now twice as big).  Note that,
  // in addition to resizing the images, these functions also make the
  // appropriate adjustments to the face boxes so that they still fall on
  // top of the faces after the images are resized.
  dlib::upsample_image_dataset<dlib::pyramid_down<2> >(img_train, anno_train);
  dlib::upsample_image_dataset<dlib::pyramid_down<2> >(img_test,  anno_test);
  // Since human faces are generally left-right symmetric we can increase
  // our training dataset by adding mirrored versions of each image back
  // into img_train.  So this next step doubles the size of our
  // training dataset.  Again, this is obviously optional but is useful in
  // many object detection tasks.
  add_image_left_right_flips(img_train, anno_train);
  std::cout << "num training images: " << img_train.size() << std::endl;
  std::cout << "num testing images:  " << img_test.size() << std::endl;
  // Finally we get to the training code.  dlib contains a number of
  // object detectors.  This typedef tells it that you want to use the one
  // based on Felzenszwalb's version of the Histogram of Oriented
  // Gradients (commonly called HOG) detector.  The 6 means that you want
  // it to use an image pyramid that downsamples the image at a ratio of
  // 5/6.  Recall that HOG detectors work by creating an image pyramid and
  // then running the detector over each pyramid level in a sliding window
  // fashion.
  image_scanner_type scanner;
  // The sliding window detector will be 80 pixels wide and 80 pixels tall.
  scanner.set_detection_window_size(60, 80);
  dlib::structural_object_detection_trainer<image_scanner_type> trainer(scanner);
  // Set this to the number of processing cores on your machine.
  trainer.set_num_threads(4);
  // The trainer is a kind of support vector machine and therefore has the usual SVM
  // C parameter.  In general, a bigger C encourages it to fit the training data
  // better but might lead to overfitting.  You must find the best C value
  // empirically by checking how well the trained detector works on a test set of
  // images you haven't trained on.  Don't just leave the value set at 1.  Try a few
  // different C values and see what works best for your data.
  trainer.set_c(1);
  // We can tell the trainer to print it's progress to the console if we want.
  trainer.be_verbose();
  // The trainer will run until the "risk gap" is less than 0.01.  Smaller values
  // make the trainer solve the SVM optimization problem more accurately but will
  // take longer to train.  For most problems a value in the range of 0.1 to 0.01 is
  // plenty accurate.  Also, when in verbose mode the risk gap is printed on each
  // iteration so you can see how close it is to finishing the training.
  trainer.set_epsilon(0.01);

  // Now we run the trainer.  For this example, it should take on the order of 10
  // seconds to train.
  dlib::object_detector<image_scanner_type> detector = trainer.train(img_train, anno_train);

  // Like everything in dlib, you can save your detector to disk using the
  // serialize() function.
  dlib::serialize("../../data/models/detector_mtb.svm") << detector;

  //evaluate_dlib_detector(detector, img_train, img_test, anno_train, anno_test);
}

void Dlib_fhog::load_dlib_detector()
{
  // Then you can recall it using the deserialize() function.
  dlib::deserialize("../../data/models/detector_mtb.svm") >> detector;

}

/*
void Dlib_fhog::evaluate_dlib_detector(dlib::object_detector<image_scanner_type> detector, dlib::array<dlib::array2d<unsigned char> > img_train, dlib::array<dlib::array2d<unsigned char> > img_test, std::vector<std::vector<dlib::rectangle> > anno_train,  std::vector<std::vector<dlib::rectangle> > anno_test)
{

  // Now that we have a face detector we can test it.  The first statement tests it
  // on the training data.  It will print the precision, recall, and then average precision.
  std::cout << "training results: " << dlib::test_object_detection_function(detector, img_train, anno_train) << std::endl;
  // However, to get an idea if it really worked without overfitting we need to run
  // it on images it wasn't trained on.  The next line does this.  Happily, we see
  // that the object detector works perfectly on the testing images.
  std::cout << "testing results:  " << dlib::test_object_detection_function(detector, img_test, anno_test) << std::endl;

}

void Dlib_fhog::execute_dlib_detector(cv::Mat input_img)
{
  std::vector<dlib::rectangle> dets = detector(input_img);
  std::cout << dets[0].top() << std::endl;
}
*/
