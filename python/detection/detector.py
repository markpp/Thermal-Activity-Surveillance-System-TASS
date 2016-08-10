import os
import sys
import glob

import dlib
from skimage import io

class detector:

    def __init__(self, detector_path):
        print "Loading detector..."
        self.detector = dlib.simple_object_detector("../data/models/detector.svm")

    def show_learned_hog_filter(self):
        # Now let's use the detector as you would in a normal application.  First we
        # will load it from disk.
        #print "Loading detector"

        #detector = dlib.simple_object_detector("../data/models/detector.svm")

        # We can look at the HOG filter we learned.  It should look like a face.  Neat!
        win_det = dlib.image_window()
        win_det.set_image(self.detector)
        dlib.hit_enter_to_continue()

    def dlib_detector(self, img):
        # Now let's use the detector as you would in a normal application.  First we
        # will load it from disk.
        #detector = dlib.simple_object_detector("../data/models/detector.svm")

        # Now let's run the detector over the images in the faces folder and display the
        # results.
        #win = dlib.image_window()

        dets = self.detector(img)
        print("Number of objects detected: {}".format(len(dets)))

        #win.clear_overlay()
        #win.set_image(img)
        #win.add_overlay(dets)
        #dlib.hit_enter_to_continue()

        #io.imshow(img)
        #io.show()
        return dets

