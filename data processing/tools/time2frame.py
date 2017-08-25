import os
import time
from datetime import datetime
import calendar
import argparse
import numpy as np
from path_checker import check_path
               
if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
    args = vars(ap.parse_args())

    path = check_path(args["path"]) #2016-08-10
    startSeconds = calendar.timegm(time.strptime('Aug 10, 2016 @ 11:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    #path = '/Volumes/WD1TBNTFS/output/output27sep.csv'
    with open(path) as inputfile:
        for line in inputfile:  
            curr_time = line.split('\n')[0];
            #time_dec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + curr_time.split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + curr_time.split('.')[1]))
            time_dec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + curr_time + ' UTC', '%b %d, %Y @ %H:%M:%S UTC'))
            frame = int(round((time_dec - startSeconds)) * 9);
            
            print(curr_time + ' - ' + str(frame))

   