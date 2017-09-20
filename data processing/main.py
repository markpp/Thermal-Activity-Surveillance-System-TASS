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
import persons
import tracking


if __name__ == "__main__":
    """Main function for executing the primary components of the program.

    System parameters are loaded from file and passed to xx,
    where data structures are defined and various xx implementations are executed:

    main.py -p ../data/testing/2016-08-09-14-58-testing/ -a ../data/annotations/bb/2016-08-09-14-58_bb.csv -f 723
    """

    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str, default='',
                    help="(optional) Path to frames")
    ap.add_argument("-a", "--anno", type=str, default='',
                    help="(optional) path to annotations")
    ap.add_argument("-f", "--frame", type=int, default=0,
                    help="(optional) start frame number")
    args = vars(ap.parse_args())

    # Force window location, useful for multi screen setups
    cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Preview', 0, 200)

    # Prepare path to frames
    frames_dir = args["path"]
    if not frames_dir:
        print("No path to frames given.")
    else:
        frames_dir = tools.path_checker.check_path(frames_dir)

    # Prepare annotations
    annotations = {}
    if args["anno"]:
        annotations = tools.file_handler.read_annotations(args["anno"])
    else:
        print("No path to annotation file given.")

    start_frame = args["frame"]

    # Train the detectors
    #detection.detect.train_detector()

    #print(sorted(tools.list_frames_in_dir.list_frames(frames_dir)))
    # Run the detectors on the provided data
    # detection.detect.detect_hog(frames_dir, start_frame, sorted(annotations))
    #detection.detect.detect_hog(frames_dir, start_frame, sorted(tools.list_frames_in_dir.list_frames(frames_dir)))

    # Run detctor with tracking enabled
    detection.detect.detect_hog_tracked(frames_dir, start_frame, sorted(tools.list_frames_in_dir.list_frames(frames_dir)))

    # Previews only frames with annotations
    #presentation.preview.annotation_preview(frames_dir, annotations, start_frame, 1.0)

    # Requires a continous list of frames
    #presentation.preview.continous_preview(start_frame, frames_dir, annotations, 4.0)
