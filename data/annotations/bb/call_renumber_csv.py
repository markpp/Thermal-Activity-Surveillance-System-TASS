"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys
sys.path.append('../../../data processing/tools/')
from renumber_csv_annotations import renumber_csv


def fix_numbering():

    # train
    renumber_csv('training/2015-09-02-12-44_bb.csv', -4233)
    renumber_csv('training/2015-09-28-12-39_bb.csv', 0)
    renumber_csv('training/2016-08-08-11-00_bb.csv', 0)

    # test
    renumber_csv('testing/2015-09-30-06-23_bb.csv', 0)
    renumber_csv('testing/2015-10-05-15-56_bb.csv', 0)
    renumber_csv('testing/2016-08-09-14-58_bb.csv', 0)

if __name__ == '__main__':
    """Main function for executing the run script.

    """
    fix_numbering()
