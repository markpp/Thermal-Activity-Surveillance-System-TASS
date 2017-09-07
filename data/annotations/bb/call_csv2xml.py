"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys
sys.path.append('../../../data processing/tools/')
from csv2xml import convert


if __name__ == '__main__':
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    """

    # train
    convert('training/2016-08-08-11-00_bb.csv', '/home/markpp/Desktop/code/mtb/data/train/2016-08-08-11-00', 1)
    convert('training/2015-09-02-12-44_bb.csv', '/home/markpp/Desktop/code/mtb/data/train/2015-09-02-12-44', 1)
    convert('training/2015-09-28-12-39_bb.csv', '/home/markpp/Desktop/code/mtb/data/train/2015-09-28-12-39', 1)

    # test
    convert('testing/2015-09-30-06-23_bb.csv', '/home/markpp/Desktop/code/mtb/data/train/2015-09-30-06-23', 1)
    convert('testing/2015-10-05-15-56_bb.csv', '/home/markpp/Desktop/code/mtb/data/train/2015-10-05-15-56', 1)
    #convert('2016-08-09-14-58_bb.csv', '/home/markpp/Desktop/code/mtb/data/train/2016-08-09-14-58', 1)
