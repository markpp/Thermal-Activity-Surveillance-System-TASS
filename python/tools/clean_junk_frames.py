import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to frames")
    ap.add_argument("-e", "--end", type=int,
                    help="end frame, removes everything after this one")
    args = vars(ap.parse_args())

    path = args["path"]

    end_num = args["end"]

    for filename in os.listdir(path):
        print filename
        #prefix, num = filename[:-4].split('_')
        name, postfix = filename[:].split('.')
        if (postfix == 'png'):
            prefix, num =name[:].split('_')
            if(int(num) > end_num):
                print num
                os.remove(os.path.join(path, filename))
                #new_filename = "frame_" + num.zfill(6) + ".png"
                #os.rename(os.path.join(path, filename), os.path.join(path, new_filename))

