"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys

if __name__ == '__main__':
    """Main function for executing the run script.

    """
    os.system("python graph_events.py -e 2015-10-05-15-56_event.csv -t 2015-10-05-15-56_tracks.csv")

    os.system("python graph_events.py -e 2016-08-09-14-58_event.csv -t 2016-08-09-14-58_tracks.csv")

    os.system("python graph_events.py -e 2015-09-30-06-23_event.csv -t 2015-09-30-06-23_tracks.csv")
