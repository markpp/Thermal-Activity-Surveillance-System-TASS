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
    Main function for executing the tracking_time_plot.py script. 
    
    Plot the graph for Tracking annotations against time 
    
    Command: 
        -p path/to/csv 
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/2015-09-02-12-44_log.csv' 
            
    """
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-pe", "--eventpath", type=str,
                    help="Path to event 'csv' file")
    ap.add_argument("-pt", "--trackpath", type=str,
                    help="Path to tracked 'csv' file")
    args = vars(ap.parse_args())

    path = args["trackpath"]
    event_path = args["eventpath"]
    startSeconds = calendar.timegm(time.strptime('Aug 10, 2016 @ 11:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    
    data = pd.read_csv(path, delimiter=';',dtype=str, names = ["Frame", "Tag", "Exit"])
    data['df_index'] = data.index
    data = data.sort_values(["Tag", "df_index"], ascending=[True, True])
    
    data = [rows for _, rows in data.groupby('Tag')]
    
    data_mtb = data[0]['Frame']
    
    #this have to be changed to be an intelligent system
    if len(data) == 2:
        data_ped = data[1]['Frame']
    
    data_frames_mtb = pd.DataFrame(data_mtb,dtype='str');
    y_val_mtb = []
    x_val_mtb = []
    
    end_time_mtb = int(round_next20min(startSeconds + float(int(data_frames_mtb.iloc[-1]['Frame']) / 9)))
    count = 0
    for x in range(startSeconds, end_time_mtb, 1200000):
        count_frame = 0
        while True:
            point = (data_frames_mtb.iloc[count_frame]['Frame'])
            timePointSec = int(startSeconds + float(int(point)) / 9)
            x_val_mtb.append(timePointSec);
            data_frames_mtb.drop(data_frames_mtb.index[count_frame])
            count_frame += 1
            y_val_mtb.append(count_frame);
            #Check next frame time
            if count_frame < len(data_frames_mtb):
                point = (data_frames_mtb.iloc[count_frame]['Frame'])
                timePointSec = startSeconds + float(int(point)) / 9
                if timePointSec >= (x + 1200000):
                    break
            else:
                break
    
    if 'data_ped' in locals():
        data_frames_ped = pd.DataFrame(data_ped,dtype='str');
        y_val_ped = []
        x_val_ped = []
        
        end_time_ped = int(round_next20min(startSeconds + float(int(data_frames_ped.iloc[-1]['Frame']) / 9)))
        count = 0
        for x in range(startSeconds, end_time_ped, 1200000):
            count_frame = 0
            while True:
                point = (data_frames_ped.iloc[count_frame]['Frame'])
                timePointSec = int(startSeconds + float(int(point)) / 9)
                x_val_ped.append(timePointSec);
                data_frames_ped.drop(data_frames_ped.index[count_frame])
                count_frame += 1
                y_val_ped.append(count_frame);
                
                #Check next frame time
                if count_frame < len(data_frames_ped):
                    point = (data_frames_ped.iloc[count_frame]['Frame'])
                    timePointSec = startSeconds + float(int(point)) / 9
                    if timePointSec >= (x + 1200000):
                        break
                else:
                    break
                
    event_data = pd.read_csv(event_path, delimiter=';',dtype=str)
    event_data['df_index'] = event_data.index
        
    event_data_mtb = event_data[['MTB']]
    event_data_ped = event_data[['PED']]
    
    event_data_frames_mtb = pd.DataFrame(event_data_mtb,dtype='str');
    event_data_frames_mtb = event_data_frames_mtb[~event_data_frames_mtb.isin(['nan']).any(axis=1)]
    event_y_val_mtb = []
    event_x_val_mtb = []
    
    end_time_mtb = int(round_next20min(calendar.timegm(time.strptime('Aug 10, 2016 @ ' + str(' '.join(map(str, event_data_frames_mtb.iloc[-1].values))).split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + str(' '.join(map(str, event_data_frames_mtb.iloc[-1].values))).split('.')[1]))))
    count = 0
    for x in range(startSeconds, end_time_mtb, 1200000):
        count_frame = 0
        while True:
            timePointSec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + str(' '.join(map(str, event_data_frames_mtb.iloc[count_frame].values))).split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + str(' '.join(map(str, event_data_frames_mtb.iloc[count_frame].values))).split('.')[1]))
            event_x_val_mtb.append(timePointSec);
            event_data_frames_mtb.drop(event_data_frames_mtb.index[count_frame])
            count_frame += 1
            event_y_val_mtb.append(count_frame);
            #Check next frame time
            if count_frame < len(event_data_frames_mtb):
                timePointSec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + str(' '.join(map(str, event_data_frames_mtb.iloc[count_frame].values))).split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + str(' '.join(map(str, event_data_frames_mtb.iloc[count_frame].values))).split('.')[1]))
                if timePointSec >= (x + 1200000):
                    break
            else:
                break
    
    event_data_frames_ped = pd.DataFrame(event_data_ped,dtype='str');
    event_data_frames_ped = event_data_frames_ped[~event_data_frames_ped.isin(['nan']).any(axis=1)]
    event_y_val_ped = []
    event_x_val_ped = []
    
    end_time_ped = int(round_next20min(calendar.timegm(time.strptime('Aug 10, 2016 @ ' + str(' '.join(map(str, event_data_frames_ped.iloc[-1].values))).split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + str(' '.join(map(str, event_data_frames_ped.iloc[-1].values))).split('.')[1]))))
    count = 0
    for x in range(startSeconds, end_time_ped, 1200000):
        count_frame = 0
        while True:
            timePointSec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + str(' '.join(map(str, event_data_frames_ped.iloc[count_frame].values))).split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + str(' '.join(map(str, event_data_frames_ped.iloc[count_frame].values))).split('.')[1]))
            event_x_val_ped.append(timePointSec);
            event_data_frames_ped.drop(event_data_frames_ped.index[count_frame])
            count_frame += 1
            event_y_val_ped.append(count_frame);
            
            #Check next frame time
            if count_frame < len(event_data_frames_ped):
                timePointSec = calendar.timegm(time.strptime('Aug 10, 2016 @ ' + str(' '.join(map(str, event_data_frames_ped.iloc[count_frame].values))).split('.')[0] + ' UTC', '%b %d, %Y @ %H:%M:%S UTC')) + (float('0.' + str(' '.join(map(str, event_data_frames_ped.iloc[count_frame].values))).split('.')[1]))
                if timePointSec >= (x + 1200000):
                    break
            else:
                break
    
    event_x_val_mtb = [dt.datetime.fromtimestamp(ts) for ts in event_x_val_mtb];
    event_x_val_ped = [dt.datetime.fromtimestamp(ts) for ts in event_x_val_ped];
    
    datenums_mtb=np.array(md.date2num(event_x_val_mtb))
    values_mtb= np.array(event_y_val_mtb);
    datenums_ped=np.array(md.date2num(event_x_val_ped))
    values_ped= np.array(event_y_val_ped);
    
    ax=plt.gca()
    xfmt = md.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    
    event_mtb_leg, = plt.plot(datenums_mtb,values_mtb, 'b-', label='MTB (manual)')
    event_ped_leg, = plt.plot(datenums_ped,values_ped, 'm-', label='PED (manual)')
    
    x_val_mtb = [dt.datetime.fromtimestamp(ts) for ts in x_val_mtb];
    datenums_mtb=np.array(md.date2num(x_val_mtb))
    values_mtb= np.array(y_val_mtb); 
    mtb_leg, = plt.plot(datenums_mtb,values_mtb, 'c--', label='MTB (system)')
    plt.legend(handles=[event_mtb_leg, mtb_leg, event_ped_leg])
   
    if 'data_ped' in locals():
        x_val_ped = [dt.datetime.fromtimestamp(ts) for ts in x_val_ped];
        datenums_ped=np.array(md.date2num(x_val_ped))
        values_ped= np.array(y_val_ped);  
        ped_leg, = plt.plot(datenums_ped,values_ped, 'r--', label='PED (system)')
        plt.legend(handles=[event_mtb_leg, mtb_leg, event_ped_leg, ped_leg])
    
    plt.ylabel('Tracking Events')
    plt.xlabel('Time')
    plt.title('Incremental activity every 20 minutes')
    plt.show()
