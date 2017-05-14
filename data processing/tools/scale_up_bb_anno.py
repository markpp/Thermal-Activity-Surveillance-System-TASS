import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
import scipy
import sys
sys.path.append('../')
import tools

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]


def check_path(path):
    # check if path ends with a "/" and remove it
    if path.endswith("/"):
        return path
    else:
        return path +'/'

if __name__ == "__main__":
    """
    Main function for executing the scale_up.py script.

    Upsacle images by a scaling factor and save a grayscale image.

    python scale_up_bb_anno.py -p /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/training/2015-09-28-12-39 -a /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/annotations/bb/2015-09-28-12-39_bb.csv -s 4
    
    Command:
        -p path/to/images [-s #]
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/'

    Output File Path:
        path/to/image/folder/4x
        '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/4x'

    Note:
        Default scaling factor is 4

    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
    ap.add_argument("-a", "--anno", type=str,
                  help="Path to bb annotations")
    ap.add_argument("-s", "--scale", type=int, default=4,
                  help="(optional) scale factor")
    args = vars(ap.parse_args())

    path = check_path(args["path"])

    annotations = {}
    if args["anno"]:
        annotations = tools.file_handler.read_annotations(args["anno"])
    else:
        print "No path to annotation file given."

    imagePath = ""

    output_path = path.rsplit('/', 2)[0] + "/4x/"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for frame in sorted(annotations):
        frame = "frame_"+ frame + ".png"
        img_path = os.path.join(path, frame)
        print img_path
        img = cv2.imread(img_path,-1)
        if not hasattr(img, 'astype'):
          print 'not image'
          print imagePath
          break
        img = cv2.resize(img, dsize=(0, 0), fx=args["scale"], fy=args["scale"])
        img = np.clip(img, 0, 8191)
        img = (img/4).astype(np.uint8)
        cv2.imwrite(os.path.join(output_path, frame), img)
