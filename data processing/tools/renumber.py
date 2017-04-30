import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2

if __name__ == "__main__":
    
    """
    Main function for executing the renumber.py script. 
    
    Rename files to start from 0 starting from a given frame and ending at the given frame 
        
    Command: 
        -p path/to/images -s startFrame -e endFrame 
        -p /Users/markpp/Desktop/code/data/test -s 12 -e 18
    """
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to frames")
    ap.add_argument("-s", "--start", type=int,
                    help="start frame, ignores everything before")
    ap.add_argument("-e", "--end", type=int,
                    help="end frame, ignores everything after")
    args = vars(ap.parse_args())

    path = args["path"]
    start_num = args["start"]
    end_num = args["end"]

    new_path = path.rsplit('/',1)[0]+"/new"

    print new_path

    for filename in os.listdir(path):
        #print filename
        #prefix, num = filename[:-4].split('_')
        name, postfix = filename[:].split('.')
        if (postfix == 'png'):
            prefix, num =name[:].split('_')
            if(int(num) >= start_num and int(num) <= end_num):
                new_num = int(num)-start_num
                print "copying frame: {}, now called: {}".format(num, str(new_num).zfill(6))
                #os.remove(os.path.join(path, filename))
                new_filename = "frame_" + str(new_num).zfill(6) + ".png"
                os.rename(os.path.join(path, filename), os.path.join(new_path, new_filename))

