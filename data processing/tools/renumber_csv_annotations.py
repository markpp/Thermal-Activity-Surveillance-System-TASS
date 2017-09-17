"""
Sample script to convert an csv annotation file into a xml file.
"""

import csv
import os
import argparse


def renumber_csv(csv_path, offset):
    print("Chaging numbering in csv...")
    csvData = csv.reader(open(csv_path))

    next(csvData)
    with open(csv_path[:-4]+'_fixed.csv', 'w') as text_file:
        text_file.write("Filename;Object ID;Annotation tag;Upper left corner X;Upper left corner Y;Lower right corner X;Lower right corner Y;\n")
        for line in csvData:
            # tag check
            old_frame_nr = int(line[0].split('_')[1].split('.')[0])
            new_frame_nr = old_frame_nr+offset
            new_frame_name = 'frame_{:06d}.png'.format(new_frame_nr)
            text_file.write(new_frame_name+';'+
                            line[0].split(';')[1]+';'+
                            line[0].split(';')[2]+';'+
                            line[0].split(';')[3]+';'+
                            line[0].split(';')[4]+';'+
                            line[0].split(';')[5]+';'+
                            line[0].split(';')[6]+';\n')

if __name__ == '__main__':
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    python csv2xml.py -c /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.csv -x /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.xml -s 4

    python csv2xml.py -c /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/annotations/bb/2015-09-02-12-44_bb.csv -x /Users/markpp/Documents/github/Thermal-Activity-Surveillance-System-TASS/data/annotations/bb/2015-09-02-12-44_bb.xml -s 4

    """

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--csv", type=str,
                    help="Path csv file")
    ap.add_argument("-o", "--offset", type=int,
                    help="Frame nr offset")
    args = vars(ap.parse_args())

    renumber_csv(args["csv"], args["offset"])
