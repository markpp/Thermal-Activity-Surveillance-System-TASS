import argparse
import numpy as np
import cv2
import csv
import os
import logging

from matplotlib import pyplot as plt
from path_checker import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class config:
    """
        Simple configuration class with the data the is required to run the script
    """
    def __init__(self):
        size = 240, 320, 3

        self.first = True
        self.last = False
        self.hotPixelCountSum = 0
        self.mask12LSB = np.zeros(size, dtype=np.uint16) + 1023
        self.activity = False
        self.frameNumber = 0
        self.lastFrameWithDetection = 0
        self.firstFrameWithDetection = 0
        self.firstDetection = 0
        self.fileFormat = '{:06d}'
conf = config();


def activity(img8U, csvWriter):
    """
        Converts the frame to grayscale and detect and object using a histogram and thresholds,
        and add new entries to the CSV file if activity is found.
    """

    histSize = [256]
    histRange = [0, 256]
    uniform = True; accumulate = False
    hotPixelCount = 0

    hist = cv2.calcHist([img8U], [0], None, histSize, histRange, uniform, accumulate)
    min, max, min_loc, max_loc = cv2.minMaxLoc(hist)

    #print(img8U.shape)
    rows, cols = img8U.shape

    for i in range(0, rows):
        for j in range(0, cols):
          if img8U[i, j] > max_loc[1]:
            hotPixelCount += 1

    if hotPixelCount > 9:

        if not conf.activity:
            conf.firstFrameWithDetection = conf.frameNumber
        conf.activity = True
        conf.lastFrameWithDetection = conf.frameNumber
        if conf.first:
            conf.firstDetection = conf.frameNumber
        conf.first = False
        conf.last = True
        conf.hotPixelCountSum += hotPixelCount

    else:
        conf.activity = False

    if conf.lastFrameWithDetection - conf.firstFrameWithDetection > 9 and conf.last and conf.hotPixelCountSum > 50 and not conf.activity:
        conf.first = True
        logger.info("frame_" + conf.fileFormat.format(conf.firstDetection) + ".png" + ";" + "frame_" + conf.fileFormat.format(conf.lastFrameWithDetection) + ".png" + ";" + str(conf.hotPixelCountSum))
        csvWriter.writerow(["frame_" + conf.fileFormat.format(conf.firstDetection) + ".png", "frame_" + conf.fileFormat.format(conf.lastFrameWithDetection) + ".png", str(conf.hotPixelCountSum)])
        conf.hotPixelCountSum = 0
        conf.last = False
    # activityWriter(hotPixelCount)

if __name__ == "__main__":
    """
    Main function for executing the framesofInterest.py script. Which gathers the frames in which activity is found and write them to the a CSV file.

    Command:
        -p path/to/images -a path/to/save_annotations/filename
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/4x'  -a '/home/louise/Documents/MountainBike/data/annotations/2015-09-02-12-44.csv'

    Output File Format:

        StartingFrame;EndFrame;PixelChangeCount
        frame_002916.png;frame_003877.png;29988470
    Note:
        If run on Linux path have to be without spaces or with '\' before the space

    """
    first = True
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
    ap.add_argument("-a", "--activity_file", type=str,
                    help="Path to save CSV file")
    args = vars(ap.parse_args())

    path = check_path(args["path"])
    csv_path = args["activity_file"]

    show = 1

    frame_list = os.listdir(path)
    print("Number of frames: {}".format(len(frame_list))
    with open(csv_path, 'w+') as csvFile:
        csvWriter = csv.writer(csvFile)
        # Loop through the folders to get frames
        for frame in range(0, len(frame_list) - 1):
            imageFileName = path + "/" + "frame_" + conf.fileFormat.format(frame) + ".png"
            conf.frameNumber = frame
            img = cv2.imread(imageFileName, 0)

            if img is None:
                logger.error("File: " + imageFileName + " , not found!")
                break

            if(show):
                output = img.copy()
                cv2.putText(output,str(frame),(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.2,255,1,cv2.LINE_AA)
                cv2.imshow('image',output)
                cv2.waitKey(1)
            activity(img, csvWriter);
