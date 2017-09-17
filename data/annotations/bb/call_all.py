"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys

if __name__ == '__main__':
    """Main function for executing the run script.

    """

    os.system('python call_renumber_csv.py')
    os.system('python call_scale_bb_annotations.py')
    os.system('python call_csv2xml.py')
    os.system('python call_append_xml.py')
