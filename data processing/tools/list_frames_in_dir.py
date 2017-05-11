import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2

def list_frames(path):
    frame_nr_list = []
    for filename in os.listdir(path):
        #print filename
        #prefix, num = filename[:-4].split('_')
        name, postfix = filename[:].split('.')
        if (postfix == 'png'):
            prefix, num =name[:].split('_')
            frame_nr_list.append(num)
    return frame_nr_list

if __name__ == "__main__":
    """
    Main function for executing the .py script.

    Command:
        -p path/to/images
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/' -e 5034

    """
    #python clean_junk_frames.py -p /Volumes/WD1TBNTFS/MTBdata/test -e 8
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to frames")
    ap.add_argument("-e", "--end", type=int,
                    help="end frame, removes everything after this one")
    args = vars(ap.parse_args())

    print(list_frames(args["path"]))


                #new_filename = "frame_" + num.zfill(6) + ".png"
                #os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
