import argparse
import numpy as np
import cv2
import csv
import os
import logging
import random
from matplotlib import pyplot as plt

def plot(events):

    #data = np.random.normal(0, 20, 1000)


    # fixed bin size
    bins = np.arange(0, max(events), int(max(events)/10)) # fixed bin size

    plt.xlim([0-5, max(events)+5])

    plt.hist(events, bins=bins, alpha=0.5, cumulative=True)
    plt.title('Event detections')
    plt.xlabel('frame nr')
    plt.ylabel('counts')

    plt.show()


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

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--event_path", type=str,
                  help="Path to frames")
    args = vars(ap.parse_args())

    csv_path = args["event_path"]

    events = []
    with open(csv_path, 'rb') as csvfile:
        eventreader = csv.reader(csvfile, delimiter=';')
        for event in eventreader:
            frame_nr = int(event[0].split('.')[0].split('_')[1])
            events.append(frame_nr)

    plot(events)
