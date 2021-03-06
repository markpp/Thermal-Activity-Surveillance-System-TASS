import glob
import os
import sys
import time
import calendar
import csv
import argparse
from path_checker import check_path

startPoints = []
startTimes = []

if __name__ == "__main__":
    """
        Main function for executing the frame_number2time.py script.

        Converts the frame-based CSV timeseries annotations into a useful UTC formated time for first frame with activity

        Command:
            -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/' -o '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/out.txt'
            
            python frame_number2time_stamp.py -p ../../data/annotations/activity/2015-09-30-06-23_activity.csv -o ../../data/annotations/activity/generated_time_stamps/2015-09-30-06-23_activity.txt
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
    ap.add_argument("-o", "--outpath", type=str, default=4,
                  help="File Results Path")
    args = vars(ap.parse_args())

    path = check_path(args["path"]) #2016-08-10
    outpath = check_path(args["outpath"])
    startSeconds = calendar.timegm(time.strptime('Aug 10, 2016 @ 11:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    #path = '/Volumes/WD1TBNTFS/output/output27sep.csv'
    with open(path) as inputfile:
        for line in inputfile:
            print(line)
            startPoints.append(line[:-4].split('_')[1].split('.')[0])

    with open(outpath, 'w') as text_file:
        for point in startPoints:
            timePointSec = startSeconds + float(int(point)) / 9
            #print timePoint
            timePoint = time.gmtime(timePointSec)
            timeString = str(timePoint.tm_year).zfill(4) + '-' + str(timePoint.tm_mon).zfill(2) + '-' + str(timePoint.tm_mday).zfill(2) + ' ' + str(timePoint.tm_hour).zfill(2) + ':' + str(timePoint.tm_min).zfill(2) + ':' + str(timePoint.tm_sec).zfill(2) + '\n'
            text_file.write(timeString)


    #print startTimes
