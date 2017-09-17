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
    convert('training/2016-08-08-11-00_bb_fixed.csv', '/home/markpp/Desktop/code/mtb/data/train/2016-08-08-11-00/2x', 1)
    convert('training/2015-09-02-12-44_bb_fixed.csv', '/home/markpp/Desktop/code/mtb/data/train/2015-09-02-12-44/2x', 1)
    convert('training/2015-09-28-12-39_bb_fixed.csv', '/home/markpp/Desktop/code/mtb/data/train/2015-09-28-12-39/2x', 1)

    # test
    #convert('testing/2015-09-30-06-23_bb_fixed.csv', '/home/markpp/Desktop/code/mtb/data/test/2015-09-30-06-23/2x', 1)
    #convert('testing/2015-10-05-15-56_bb_fixed.csv', '/home/markpp/Desktop/code/mtb/data/test/2015-10-05-15-56/2x', 1)
    #convert('testing/2016-08-09-14-58_bb_fixed.csv', '/home/markpp/Desktop/code/mtb/data/test/2016-08-09-14-58/2x', 1)
