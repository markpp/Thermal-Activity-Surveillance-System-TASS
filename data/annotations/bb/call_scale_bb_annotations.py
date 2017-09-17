"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys
sys.path.append('../../../data processing/tools/')
from scale_bb_annotations import read_annotations


if __name__ == '__main__':
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    """

    # train
    #read_annotations('training/2016-08-08-11-00_bb.csv', 2, 80, 60)
    #read_annotations('training/2015-09-02-12-44_bb.csv', 2, 80, 60)
    #read_annotations('training/2015-09-28-12-39_bb.csv', 2, 80, 60)

    read_annotations('training/2016-08-08-11-00_bb_fixed.csv', 2, 80, 60)
    read_annotations('training/2015-09-02-12-44_bb_fixed.csv', 2, 80, 60)
    read_annotations('training/2015-09-28-12-39_bb_fixed.csv', 2, 80, 60)

    # test
    #read_annotations('testing/2015-09-30-06-23_bb.csv', 0.5, 80, 60)
    #read_annotations('testing/2015-10-05-15-56_bb.csv', 0.5, 80, 60)
    #read_annotations('testing/2016-08-09-14-58_bb.csv', 0.5, 80, 60)

    read_annotations('testing/2015-09-30-06-23_bb_fixed.csv', 0.5, 80*4, 60*4)
    read_annotations('testing/2015-10-05-15-56_bb_fixed.csv', 0.5, 80*4, 60*4)
    read_annotations('testing/2016-08-09-14-58_bb_fixed.csv', 0.5, 80*4, 60*4)
