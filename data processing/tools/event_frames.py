import os
import csv
import cv2
import time
from datetime import datetime
import calendar
import argparse
import numpy as np
               
if __name__ == "__main__":
    """
    Main function for executing the event_frames.py script. 
    
    Display the frames with events 
    
    Command: 
        -p path/to/csv -o path/to/output/folder -i path/to/image/folder
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/2015-09-02-12-44.csv' -o '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/output' -i '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/'
            
    """
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to 'csv' file")
    ap.add_argument("-i", "--imgPath", type=str,
                    help="Path to the frame folder")
    ap.add_argument("-o", "--outPath", type=str,
                    help="Path to output video")
    args = vars(ap.parse_args())

    path = args["path"]
    out_path = args["outPath"]
    image_path = args["imgPath"]
        
    start_seconds = calendar.timegm(time.strptime('Aug 10, 2016 @ 11:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    mtb_times = []
    ped_times = []
    
    with open(path, 'r') as input_file:
        for line in input_file:
            mtb_times.append(line.split(';')[0])
            ped_times.append(line.split(';')[1])
            
    # Determine the width and height from the first image
    image = os.path.join(image_path, "frame_{:06d}".format(0) + ".png")
    frame_size = cv2.imread(image)
    height, width, channels = frame_size.shape
            
    video_out_mtb = cv2.VideoWriter(os.path.join(out_path, "mtb.avi"), cv2.VideoWriter_fourcc(*'XVID'), 1, (width, height), False)

    iter_mtb = iter(mtb_times)
    next(iter_mtb)
    for curr_time in iter_mtb:
        if (curr_time == ''):
            break;
        time_dec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + curr_time.split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + curr_time.split('.')[1]))
        frame = int(round((time_dec - start_seconds)) * 9);
        print(frame)
        frame_path = os.path.join(image_path, "frame_{:06d}".format(frame) + ".png");
        
        img = cv2.imread(frame_path, -1)
    
        if img is None:    
            print("Problem in mtb with reading: " + frame_path)
            continue;
        
        img = np.clip(img, 0, 8191)
        img = (img/4).astype(np.uint8)
        
        video_out_mtb.write(img)
        #cv2.imshow('test', img)
        cv2.waitKey(0);
    
    video_out_mtb.release()
    
    video_out_ped = cv2.VideoWriter(os.path.join(out_path, "ped.avi"), cv2.VideoWriter_fourcc(*'XVID'), 1, (width, height), False)

    iter_ped = iter(ped_times)
    next(iter_ped)
    for curr_time in iter_ped:
        if (curr_time == ''):
            break;
        time_dec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + curr_time.split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + curr_time.split('.')[1]))
        frame = int(round(time_dec - start_seconds) * 9);
        frame_path = os.path.join(image_path, "frame_{:06d}".format(frame) + ".png");
        
        img = cv2.imread(frame_path, -1)
            
        if img is None:    
            print("Problem in ped with reading: " + frame_path)
            print(frame)
            continue;
        
        img = np.clip(img, 0, 8191)
        img = (img/4).astype(np.uint8)
        video_out_ped.write(img)    
    
    video_out_ped.release()
    