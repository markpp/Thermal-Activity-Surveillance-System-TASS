"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys

if __name__ == '__main__':
    """Main function for executing the run script.

    """

    '''
    TPs : 45
    FNs : 2
    FPs : 6
    PED
    TPs : 3
    FNs : 1
    FPs : 5
    '''
    print("running 2015-10-05-15-56")
    os.system("python graph_events.py -e 2015-10-05-15-56_gt.csv -t 2015-10-05-15-56_tracks.csv")

    '''
    TPs : 22
    FNs : 4
    FPs : 6
    PED
    TPs : 2
    FNs : 1
    FPs : 3
    '''
    #print("running 2016-08-09-14-58")
    #os.system("python graph_events.py -e 2016-08-09-14-58_gt.csv -t 2016-08-09-14-58_tracks.csv")

    '''
    TPs : 39
    FNs : 3
    FPs : 1
    PED
    TPs : 5
    FNs : 0
    FPs : 2
    '''
    #print("running 2015-09-30-06-23")
    #os.system("python graph_events.py -e 2015-09-30-06-23_gt.csv -t 2015-09-30-06-23_tracks.csv")
