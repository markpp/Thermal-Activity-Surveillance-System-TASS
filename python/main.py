"""
This file contains the script for executing the three different Mandelbrot implementations.

"""
import time
import sys
import os
import argparse
import numpy as np
import cv2

import tools
import presentation
import detection


def continous_preview(frames_dir, annotations):
    # Consecutive preview of frames
    frame_nr_begin = args["frame"]
    for frame_nr in range(frame_nr_begin, frame_nr_begin + 1000):
        # for index in range(frameNumber, len(os.listdir(path))):
        frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
        # print frame_path
        img = cv2.imread(frame_path, -1)
        if img is not None:
            img = np.clip(img, 0, 8191)
            img = np.array(img / 4).astype(np.uint8)
            cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, 4.0))
        else:
            print 'read failed for: '
            print frame_path
        # cv2.waitKey()
        k = cv2.waitKey(33)
        if k == ord('q'):
            print "Quitting..."
            break
        elif k == ord('p'):
            print "Paused."
            cv2.waitKey()
            print "Unpaused."


def annotation_preview(frames_dir, annotations, start_frame):
    # Showing only frames with annotated objects

    frame_list = sorted(annotations)
    output_dir = "/Users/markpp/Desktop/code/VAPprojects/PythonHoG/bikes/images4x"
    # Sort the unordered dictionary and used the sorted keys to find relevant frames
    #for frame_nr in sorted(annotations):
    #for frame_nr in frame_list:
    index = 0
    while index < len(frame_list):
        frame_nr = frame_list[index]
        if int(frame_nr) < start_frame:
            index = index+1
        else:
            #print "%s: %s" % (frame_nr, annotations[frame_nr])
            frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
            # print frame_path
            img = cv2.imread(frame_path, -1)
            if img is not None:
                img = np.clip(img, 0, 8191)
                img = np.array(img / 4).astype(np.uint8)
                tools.file_handler.store_frame(img, frame_nr, 4.0, output_dir)
                cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, 4.0))
            else:
                print 'read failed for: '
                print frame_path

            k = cv2.waitKey(20)
            #print k
            if k == 32:
                index = index+1
                print "Next frame -> {}".format(int(frame_nr)+1)
            if k == ord('b'):
                index = index-1
                print "Next frame <- {}".format(int(frame_nr)-1)
            elif k == ord('q'):
                print "Quitting..."
                break
            elif k == ord('p'):
                print "Paused."
                cv2.waitKey()
                print "Unpaused."
            else:
                index = index + 1
                print "Next frame -> {}".format(int(frame_nr) + 1)


def detect_hog(frames_dir, annotations):
    # Showing only frames with annotated objects

    hog_detector = detection.detector.detector("../data/models/detector.svm")

    frame_list = sorted(annotations)
    # Sort the unordered dictionary and used the sorted keys to find relevant frames
    index = 0
    #for frame_nr in sorted(annotations):
    while index < len(frame_list):
        frame_nr = frame_list[index]
        if int(frame_nr) < start_frame:
            index = index+1
        else:
            #print "%s: %s" % (frame_nr, annotations[frame_nr])
            frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
            # print frame_path
            img = cv2.imread(frame_path, -1)
            if img is not None:
                img = np.clip(img, 0, 8191)
                img = np.array(img / 4).astype(np.uint8)
                frame = cv2.resize(img, dsize=(0, 0), fx=4.0, fy=4.0)
                #img2 = cv2.imread("/Users/markpp/Desktop/code/VAPprojects/PythonHoG/bikes/images8x/frame_004297.png", -1)
                #presentation.presenter.show_hog(frame)
                #cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, 4.0))
                detections = hog_detector.dlib_detector(frame)
                cv2.imshow('Preview', presentation.presenter.draw_detections(frame, frame_nr, detections, 4.0))

            else:
                print 'read failed for: '
                print frame_path
            # cv2.waitKey()
            k = cv2.waitKey()
            # print k
            if k == 32:
                index = index + 1
                print "Next frame -> {}".format(int(frame_nr) + 1)
            if k == ord('b'):
                index = index - 1
                print "Next frame <- {}".format(int(frame_nr) - 1)
            elif k == ord('q'):
                print "Quitting..."
                break
            elif k == ord('p'):
                print "Paused."
                cv2.waitKey()
                print "Unpaused."


if __name__ == "__main__":
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    -p /Users/markpp/Desktop/code/data/2015-09-28-12-39 -a /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.csv -f 4890
    """

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to frames")
    ap.add_argument("-a", "--anno", type=str,
                    help="(optional) path to annotations")
    ap.add_argument("-f", "--frame", type=int, default=0,
                    help="(optional) start frame")
    args = vars(ap.parse_args())

    # Force window location, useful for multi screen setups
    cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Preview', 0, 200)

    # Prepare path to frames
    frames_dir = args["path"]
    if not frames_dir:
        print "No path to frames given."
    else:
        frames_dir = tools.path_checker.check_path(frames_dir)

    # Prepare annotations
    annotations = {}
    if args["anno"]:
        annotations = tools.file_handler.read_annotations(args["anno"])
    else:
        print "No path to annotation file given."

    start_frame = args["frame"]

    #detection.detector.show_learned_hog_filter("../data/models/")
    detect_hog(frames_dir, annotations)
    #annotation_preview(frames_dir, annotations, start_frame)
    #test(frames_dir, annotations)
    #continous_preview(frames_dir, annotations)

