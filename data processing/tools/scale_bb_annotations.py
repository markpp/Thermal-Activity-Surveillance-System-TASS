import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
import scipy
import sys

def check_value(number, axis_max, frame_name):
    if number < 0:
        print("{} failed check".format(frame_name))
        number = 0
    if number > axis_max-1:
        print("{} failed check".format(frame_name))
        number = axis_max-1
    return int(number)

def read_annotations(anno_path, scale, x_axis_max, y_axis_max):
    """Read csv file with annotations into dictionary structure.

    The csv annotation file is parsed line by line and annotations are
    stored in dictionary with frame number as key:

    Args:
        anno_path (str): Path to csv file.

    Returns:
        (dict): Returns dictionary of annotations.
    """

    print("Reading annotations...")
    print(anno_path)
    csv_path = anno_path[:len(anno_path)-4] + '_scaled.csv'

    # read annotations line by line from file
    with open(anno_path) as anno_file:
        with open(csv_path, 'wb') as csvFile:
            csvWriter = csv.writer(csvFile)
            next(anno_file) # Skip header line
            csvWriter.writerow(['Filename;Object ID;Annotation tag;Upper left corner X;Upper left corner Y;Lower right corner X;Lower right corner Y;'])
            for line in anno_file:
                anno = line.split(';')
                left = check_value(int(int(anno[3])*scale), x_axis_max*scale, anno[0])
                top = check_value(int(int(anno[4])*scale), y_axis_max*scale, anno[0])
                right = check_value(int(int(anno[5])*scale), x_axis_max*scale, anno[0])
                bottom = check_value(int(int(anno[6])*scale), y_axis_max*scale, anno[0])

                csvWriter.writerow([anno[0] + ';' + \
                                    anno[1] + ';' + \
                                    anno[2] + ';' + \
                                    str(left) + ';' + \
                                    str(top) + ';' + \
                                    str(right) + ';' + \
                                    str(bottom) + ';'])


if __name__ == "__main__":
    """
    Main function for executing the scale_up.py script.

    Scale bounding box annotations.

    python scale_bb_annotations.py -p -a -s

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
    ap.add_argument("-a", "--anno", type=str,
                  help="Path to bb annotations")
    ap.add_argument("-s", "--scale", type=float, default=2.0,
                  help="(optional) scale factor")
    args = vars(ap.parse_args())

    if args["anno"]:
        read_annotations(args["anno"], args["scale"])
    else:
        print("No path to annotation file given.")

    # train
    read_annotations('../../data/annotations/bb/training/2016-08-08-11-00_bb.csv', 2, 80, 60)


    # test
    read_annotations('../../data/annotations/bb/testing/2015-09-30-06-23_bb.csv', 0.5, 80, 60)
