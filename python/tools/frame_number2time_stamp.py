import glob
import os
import sys
import time
import calendar
import csv

startPoints = []
startTimes = []
'''
Converts the frame-based CSV timeseries annotations into a useful UTC formated time for first frame with activity
'''
if __name__ == "__main__":
    path = sys.argv[1] #2016-08-10
    startSeconds = calendar.timegm(time.strptime('Aug 10, 2016 @ 11:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    #path = '/Volumes/WD1TBNTFS/output/output27sep.csv'
    with open(path) as inputfile:
        for line in inputfile:
            #print line
            startPoints.append(line[:-4].split('_')[1].split('.')[0])

    with open('/Users/markpp/Desktop/output.txt', 'wb') as text_file:
        for point in startPoints:
            timePointSec = startSeconds + float(int(point)) / 9
            #print timePoint
            timePoint = time.gmtime(timePointSec)
            timeString = str(timePoint.tm_year).zfill(4) + '-' + str(timePoint.tm_mon).zfill(2) + '-' + str(timePoint.tm_mday).zfill(2) + ' ' + str(timePoint.tm_hour).zfill(2) + ':' + str(timePoint.tm_min).zfill(2) + ':' + str(timePoint.tm_sec).zfill(2) + '\n'
            #startTimes.append(timeString)
            #print time.gmtime(timePointSec)
            text_file.write(timeString)


    #print startTimes
