import matplotlib.pyplot as plt
import matplotlib.dates as md
import math
import argparse
import operator
import math
import time
import calendar
import numpy as np
import pandas as pd
from numpy import dtype
import datetime as dt

def round_next20min(x):
    return int(math.ceil(x / 1200000.0)) * 1200000
               
if __name__ == "__main__":
    """
    Main function for executing the activity_time_plot.py script. 
    
    Display the frames with events 
    
    Command: 
        -p event_data/to/csv 
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/2015-09-02-12-44_bb.csv' 
            
    """
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    help="Path to 'csv' file")
    args = vars(ap.parse_args())

    event_path = args["path"]
    startSeconds = calendar.timegm(time.strptime('Aug 10, 2016 @ 11:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    
    event_data = pd.read_csv(event_path, delimiter=';',dtype=str)
    event_data['df_index'] = event_data.index
    event_data = event_data.sort_values(["Annotation tag", "df_index"], ascending=[True, True])
    
    event_data = [rows for _, rows in event_data.groupby('Annotation tag')]
    
    event_data_mtb = event_data[0]['Filename']
    event_data_ped = event_data[1]['Filename']
    
    event_data_frames_mtb = pd.DataFrame(event_data_mtb,dtype='str');
    y_val_mtb = []
    x_val_mtb = []
    
    end_time_mtb = int(round_next20min(startSeconds + float(int((event_data_frames_mtb.iloc[-1]['Filename'][:-4].split('_')[1].split('.')[0]))) / 9))
    count = 0
    for x in range(startSeconds, end_time_mtb, 1200000):
        count_frame = 0
        while True:
            point = (event_data_frames_mtb.iloc[count_frame]['Filename'][:-4].split('_')[1].split('.')[0])
            timePointSec = int(startSeconds + float(int(point)) / 9)
            x_val_mtb.append(timePointSec);
            event_data_frames_mtb.drop(event_data_frames_mtb.index[count_frame])
            count_frame += 1
            y_val_mtb.append(count_frame);
            #Check next frame time
            if count_frame < len(event_data_frames_mtb):
                point = (event_data_frames_mtb.iloc[count_frame]['Filename'][:-4].split('_')[1].split('.')[0])
                timePointSec = startSeconds + float(int(point)) / 9
                if timePointSec >= (x + 1200000):
                    break
            else:
                break
    
    event_data_frames_ped = pd.DataFrame(event_data_ped,dtype='str');
    y_val_ped = []
    x_val_ped = []
    
    end_time_ped = int(round_next20min(startSeconds + float(int((event_data_frames_ped.iloc[-1]['Filename'][:-4].split('_')[1].split('.')[0]))) / 9))
    count = 0
    for x in range(startSeconds, end_time_ped, 1200000):
        count_frame = 0
        while True:
            point = (event_data_frames_ped.iloc[count_frame]['Filename'][:-4].split('_')[1].split('.')[0])
            timePointSec = int(startSeconds + float(int(point)) / 9)
            x_val_ped.append(timePointSec);
            event_data_frames_ped.drop(event_data_frames_ped.index[count_frame])
            count_frame += 1
            y_val_ped.append(count_frame);
            
            #Check next frame time
            if count_frame < len(event_data_frames_ped):
                point = (event_data_frames_ped.iloc[count_frame]['Filename'][:-4].split('_')[1].split('.')[0])
                timePointSec = startSeconds + float(int(point)) / 9
                if timePointSec >= (x + 1200000):
                    break
            else:
                break
    
    x_val_mtb = [dt.datetime.fromtimestamp(ts) for ts in x_val_mtb];
    x_val_ped = [dt.datetime.fromtimestamp(ts) for ts in x_val_ped];
    datenums_mtb=np.array(md.date2num(x_val_mtb))
    values_mtb= np.array(y_val_mtb);
    datenums_ped=np.array(md.date2num(x_val_ped))
    values_ped= np.array(y_val_ped);
    plt.subplots_adjust(bottom=0.2)
    plt.xticks( rotation=25 )
    ax=plt.gca()
    xfmt = md.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    mtb_leg, = plt.plot(datenums_mtb,values_mtb, 'r-', label='MTB')
    ped_leg, = plt.plot(datenums_ped,values_ped, 'b-', label='PED')
    plt.legend(handles=[mtb_leg, ped_leg])
    plt.ylabel('Activity')
    plt.xlabel('Time')
    plt.title('Incremental activity every 20 minutes')
    plt.show()
