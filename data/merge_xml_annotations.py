"""
Sample script to convert an csv annotation file into a xml file.
"""

import csv
import os
import argparse

def merge(f1_path, f2_path):
    print "merging files..."

    with open(f1_path) as f1:
        lines1 = f1.readlines()
    with open(f2_path) as f2:
        lines2 = f2.readlines()

    xml_out = open("combined.xml", 'w')
    
    for line in lines1[:-2]:
        xml_out.write(line)
    for line in lines2[6:]:
        xml_out.write(line)

    xml_out.close()

if __name__ == '__main__':
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    python csv2xml.py -c /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.csv -x /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.xml -s 4

    python csv2xml.py -c /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/annotations/bb/2015-09-02-12-44_bb.csv -x /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/annotations/bb/2015-09-02-12-44_bb.xml -s 4

    python merge_xml_annotations.py -f1 /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/training/2015-09-28-12-39_bb_ped.xml -f2 /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/training/2016-08-08-11-00_bb_ped.xml 
    """

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f1", "--file1", type=str,
                    help="Path to first xml file")
    ap.add_argument("-f2", "--file2", type=str,
                    help="Path to first xml file")

    args = vars(ap.parse_args())

    merge(args["file1"], args["file2"])
