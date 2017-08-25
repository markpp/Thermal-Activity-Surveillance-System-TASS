import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import shutil
import cv2
from traitlets.config.application import catch_config_error

def copytree(src, dst, symlinks=False, ignore=None):
    try:
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if(os.path.isdir(s)):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(s, d)
    except shutil.Error as e:
        print("Directory not copied. Error: " + e)
    except OSError:
        print("Can't copy file: " + s)
            
            

if __name__ == "__main__":
    """
    Main function for executing the clean_frames.py script. 
    
    Removes all the frames after the frame specified 
    
    Command: 
        -p path/to/image/folder -o path/to/output/folder -s start_frame -e last_frame_number
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/' -o '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/output' -s 340 -e 5034
            
    """
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to frames")
    ap.add_argument("-s", "--start", type=int,
                    help="start frame, removes everything before this frame")
    ap.add_argument("-e", "--end", type=int,
                    help="end frame, removes everything after this frame")
    ap.add_argument("-o", "--outPath", type=str,
                    help="Path to output clean frames")
    args = vars(ap.parse_args())

    path = args["path"]
    out_path = args["outPath"]
    s_frame = args["start"]
    e_frame = args["end"]
    
    #Check about errors
    try:
        copytree(path, out_path);
    except:
        print("Error")
    path = out_path;
    print("Starting to delete....")
    for filename in os.listdir(path):
        name, postfix = filename[:].split('.')
        if (postfix == 'png'):
            prefix, num =name[:].split('_')
            if (int(num) < s_frame or int(num) > e_frame):
                os.remove(os.path.join(path, filename))
                continue
                
            img = cv2.imread(os.path.join(path, filename))
            
            if img is None:    
                #os.remove(os.path.join(path, filename))
                #print("removing frame: {:06d}".format(int(num)))
                shutil.copy2(os.path.join(path, prefix + '_' + (num - 1) + '.png'), os.path.join(path, filename))
                continue
    
    curr_frame = 0;    
    for frame in range(s_frame, e_frame + 1):   
            frame_path = os.path.join(path, "frame_{:06d}".format(frame) + ".png");
            new_path = os.path.join(path, "frame_{:06d}".format(curr_frame) + ".png");
            img = cv2.imread(frame_path)
            
            if img is None:
                print("File: " + frame_path + " , not found!");
                continue
            
            os.rename(frame_path, new_path);
            curr_frame += 1;
            