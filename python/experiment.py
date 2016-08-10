"""
This file contains the script for executing the three different Mandelbrot implementations.

"""
import time
import sys
import numpy as np
import cv2
import os
import argparse

import tools
import presentation
import detection


def test(frame):
    # Showing only frames with annotated objects

    #frame = cv2.resize(img, dsize=(0, 0), fx=2.0, fy=2.0)
    #detection.segmentation.background_threshold(frame)
    cv2.imshow('Preview', detection.segmentation.background_threshold(frame))
    cv2.waitKey()


if __name__ == "__main__":
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:
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

    img = cv2.imread(args["path"], -1)
    if img is not None:
        #img = np.clip(img, 0, 8191)
        #img = np.array(img / 4).astype(np.uint8)
        test(img)
    else:
        print 'read failed for: '
        print args["path"]

    #annotation_preview(frames_dir, annotations)


    #continous_preview(frames_dir, annotations)

