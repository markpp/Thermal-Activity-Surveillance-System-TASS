import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
import scipy
import sys

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
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
    ap.add_argument("-s", "--scale", type=int, default=4,
                  help="(optional) scale factor")
    args = vars(ap.parse_args())

    path = check_path(args["path"])

    imagePath = ""
    dir_list = mylistdir(path)
    imageCount = len(mylistdir(path))
    print imageCount
    output_path = "4x/"
    for frame in dir_list:
        name, postfix = frame[:].split('.')
        if (postfix == 'png'):
          img_path = os.path.join(path, frame)
          img = cv2.imread(img_path,-1)
          if not hasattr(img, 'astype'):
              print 'not image'
              print imagePath
              break
          img = cv2.resize(img, dsize=(0, 0), fx=args["scale"], fy=args["scale"])
          img = np.clip(img, 0, 8191)
          img = (img/4).astype(np.uint8)
          cv2.imwrite(os.path.join(output_path, frame), img)