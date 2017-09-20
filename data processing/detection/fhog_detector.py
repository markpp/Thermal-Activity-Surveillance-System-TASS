import os
import sys
import glob

import dlib
from skimage import io
import nms

class detector:

    def __init__(self):
        print("Detector object initialized")

    def load_dlib_detector(self):
        print("Loading detector...")
        self.detectors = [dlib.fhog_object_detector("../data/models/detector_mtb.svm"), dlib.fhog_object_detector("../data/models/detector_ped.svm")]

    def show_learned_hog_filter(self):
        # Now let's use the detector as you would in a normal application.  First we
        # will load it from disk.
        #print "Loading detector"

        #detector = dlib.simple_object_detector("../data/models/detector.svm")

        # We can look at the HOG filter we learned.  It should look like a face.  Neat!
        win_det = dlib.image_window()
        print("MTB filter")
        win_det.set_image(self.detectors[0])
        dlib.hit_enter_to_continue()
        print("PED filter")
        win_det.set_image(self.detectors[1])
        dlib.hit_enter_to_continue()

    # '''
    def det_bound_check(self, dets, scale):
        output_dets = []
        for det in dets:
            if det.left() > 0 and det.top() > 0 and det.right() < 80*scale and det.bottom() < 60*scale:
                output_dets.append(det)
        return output_dets
    # '''

    def execute_dlib_detector(self, img):

        #http://dlib.net/python/index.html#dlib.fhog_object_detector
        #dets, scores, weights = self.detectors[0].run(img)
        #dets, scores, weights = self.detectors[1].run(img)
        #import time
        #start_time = time.time()
        dets, scores, weights = dlib.fhog_object_detector.run_multiple(self.detectors, img, upsample_num_times=1, adjust_threshold=0.01)
        #print("%s" % (time.time() - start_time))
        #print(dets)
        #print(scores)
        #print(weights)
        ## dets = self.det_bound_check(dets, 2)

        if len(dets) > 1:
            nms_dets, nms_scores, nms_det_types = nms.non_max_suppression_fast(dets, scores, weights, overlapThresh=0.5)
            #print("Number of objects detected: {}".format(len(nms_dets)))
        else:
            nms_dets, nms_scores, nms_det_types = dets, scores, weights

        #print new_dets
        #win.clear_overlay()
        #win.set_image(img)
        #win.add_overlay(dets)
        #dlib.hit_enter_to_continue()

        #io.imshow(img)
        #io.show()
        return nms_dets, nms_scores, nms_det_types

    def train_dlib_detector(self):
        # Now let's do the training.  The train_simple_object_detector() function has a
        # bunch of options, all of which come with reasonable default values.  The next
        # few lines goes over some of these options.
        options = dlib.simple_object_detector_training_options()
        # Since faces are left/right symmetric we can tell the trainer to train a
        # symmetric detector.  This helps it get the most value out of the training
        # data.
        #options.add_left_right_image_flips = True # seems to degrade performance in this case
        # The trainer is a kind of support vector machine and therefore has the usual
        # SVM C parameter.  In general, a bigger C encourages it to fit the training
        # data better but might lead to overfitting.  You must find the best C value
        # empirically by checking how well the trained detector works on a test set of
        # images you haven't trained on.  Don't just leave the value set at 5.  Try a
        # few different C values and see what works best for your data.
        options.C = 9
        # Tell the code how many CPU cores your computer has for the fastest training.
        options.num_threads = 4
        options.be_verbose = True
        options.upsample_limit = 2

        # This function does the actual training.  It will save the final detector to
        # detector.svm.  The input is an XML file that lists the images in the training
        # dataset and also contains the positions of the face boxes.  To create your
        # own XML files you can use the imglab tool which can be found in the
        # tools/imglab folder.  It is a simple graphical tool for labeling objects in
        # images with boxes.  To see how to use it read the tools/imglab/README.txt
        # file.  But for this example, we just use the training.xml file included with
        # dlib.
        #options.detection_window_size = 60 * 80
        options.detection_window_size = int((50 * 70)) # 468, 1.44
        dlib.train_simple_object_detector("../data/annotations/bb/training/combined_mtb.xml", "../data/models/detector_mtb.svm", options)

        options.detection_window_size = int((40 * 90)) # 448, 2.29
        dlib.train_simple_object_detector("../data/annotations/bb/training/combined_ped.xml", "../data/models/detector_ped.svm", options)

    def evaluate_dlib_detector(self):
        # Now that we have a face detector we can test it.  The first statement tests
        # it on the training data.  It will print(the precision, recall, and then)
        # average precision.
        print("")  # Print blank line to create gap from previous output
        print("MTB detector evaluation:")
        print("Training accuracy: {}".format(dlib.test_simple_object_detector("../data/annotations/bb/training/combined_mtb.xml", "../data/models/detector_mtb.svm")))
        print("Testing accuracy: {}".format(dlib.test_simple_object_detector("../data/annotations/bb/testing/combined_mtb.xml", "../data/models/detector_mtb.svm")))

        print("PED detector evaluation:")
        print("Training accuracy: {}".format(dlib.test_simple_object_detector("../data/annotations/bb/training/combined_ped.xml", "../data/models/detector_ped.svm")))
        print("Testing accuracy: {}".format(dlib.test_simple_object_detector("../data/annotations/bb/testing/combined_ped.xml", "../data/models/detector_ped.svm")))
