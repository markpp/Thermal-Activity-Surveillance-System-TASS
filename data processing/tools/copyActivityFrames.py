import glob
import os
import argparse
import time
import calendar
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
from shutil import copyfile


def check_path(path):
    # check if path ends with a "/" and remove it

    if path.endswith("/"):
        return path[:-1]
    else:
        return path


if __name__ == "__main__":
    """Main function for executing the computActivityFrames.py script.

    The event annotation file is loaded and the frames inside the annotated intervals are
    copied to a temporary directory for bounding box annotation:

    -p /Users/markpp/Desktop/code/data/2015-09-28-12-39 -a /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.csv -f 4890
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
    ap.add_argument("-c", "--csv_path", type=str,
                    help="Path to frames")
    args = vars(ap.parse_args())

    path = check_path(args["path"])
    csv_path = args["csv_path"]
    #files = glob.glob("/media/markpp/WD1TBNTFS/MTBdata/2015-09-02-12-44(27Sep)/*.png")
    #print files[0]

    # Get frame numbers from automatic activity annotations
    frame_numbers = []
    csv_data = csv.reader(open(csv_path))
    for line in csv_data:
        start = line[0].split(';')[0].split('_')[1].split('.')[0]
        end = line[0].split(';')[1].split('_')[1].split('.')[0]
        for num in range(int(start), int(end)+1, 1):
            frame_numbers.append(num)

    #print frame_numbers
    new_path = path.rsplit('/', 1)[0] + "/extracted_frames"

    if os.path.exists(new_path):
        for frame_number in frame_numbers:
            filename = "frame_" + str(frame_number).zfill(6) + ".png"
            copyfile(os.path.join(path, filename), os.path.join(new_path, filename))
    else:
        print "output dir /extracted_frames does not exist"
    '''
    # Get frame numbers from manual event annotations
    startSeconds = 11*60*60
    print startSeconds

    csv_data = csv.reader(open(csv_path))
    next(csv_data)  # Skip header line
    for line in csv_data:
        mtb_start = line[0].split(';')[0].split(':')
        mtb_start_seconds = int(mtb_start[0])*60*60+int(mtb_start[1])*60+float(mtb_start[2])
        mtb_start_frame = int(round((mtb_start_seconds-startSeconds)*9))
        print "start: " + str(mtb_start_frame)
        mtb_end = line[0].split(';')[1].split(':')
        mtb_end_seconds = int(mtb_end[0]) * 60 * 60 + int(mtb_end[1]) * 60 + float(mtb_end[2])
        mtb_end_frame = int(round((mtb_end_seconds - startSeconds) * 9))
        print "end: " + str(mtb_end_frame)
    '''