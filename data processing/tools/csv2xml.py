"""
Sample script to convert an csv annotation file into a xml file.
"""

import csv
import os
import argparse


def mtb_annotation_check(annotation):
    # width check
    width = int(annotation[0].split(';')[5])-int(annotation[0].split(';')[3])
    if(width < 8):
        print("Annotation: {}, failed width check - {}".format(annotation[0].split(';')[0], width))
        return False

    # height check
    height = int(annotation[0].split(';')[6])-int(annotation[0].split(';')[4])
    if(height < 8):
        print("Annotation: {}, failed height check - {}".format(annotation[0].split(';')[0], height))
        return False

    # aspect ratio check
    ratio = float(width)/float(height)
    if(ratio > 0.5 and ratio < 1.0): # MTB
        return True
    else:
        print("Annotation: {}, failed ratio check - {}".format(annotation[0].split(';')[0], ratio))
        return False

def ped_annotation_check(annotation):
    # width check
    width = int(annotation[0].split(';')[5])-int(annotation[0].split(';')[3])
    if(width < 5):
        print("Annotation: {}, failed width check - {}".format(annotation[0].split(';')[0], width))
        return False

    # height check
    height = int(annotation[0].split(';')[6])-int(annotation[0].split(';')[4])
    if(height < 8):
        print("Annotation: {}, failed height check - {}".format(annotation[0].split(';')[0], height))
        return False

    # aspect ratio check
    ratio = float(width)/float(height)
    if(ratio >= 0.3 and ratio < 0.55): # PED
        return True
    else:
        print("Annotation: {}, failed ratio check - {}".format(annotation[0].split(';')[0], ratio))
        return False

def write_header(xml_file):
    xml_file.write('<?xml version="1.0" encoding="ISO-8859-1"?>' + "\n")
    xml_file.write('<?xml-stylesheet type="text/xsl" href="image_metadata_stylesheet.xsl"?>' + "\n")
    xml_file.write('<dataset>' + "\n")
    xml_file.write('<name>Training faces</name>' + "\n")
    xml_file.write('<comment>These are images from my thermal MTB dataset.</comment>' + "\n")
    xml_file.write('<images>' + '\n')

def write_footer(xml_file):
    xml_file.write('  ' + '<' + '/image' + '>' + "\n")
    xml_file.write('</images>' + "\n")
    xml_file.write('</dataset>' + "\n")

def write_annotation(line, prev_nr, first, img_path, scaling, xml_file):
    frame_nr = line[0].split('_')[1].split('.')[0]
    #print frame_nr
    if frame_nr != prev_nr:
        if not first:
            xml_file.write('  ' + '<' + '/image' + '>' + "\n")
        first = False

        xml_file.write('  ' + '<' + 'image' + ' ' + 'file' + '=' + '"' + img_path + '/' + line[0].split(';')[0] + '"' + '>' + "\n")
        prev_nr = frame_nr

    xml_file.write('    ' + '<' + 'box' + ' ' + 'top' + '=' + '"' + str(int(line[0].split(';')[4])*scaling) + '"' + ' ' +
                  'left' + '=' + '"' + str(int(line[0].split(';')[3])*scaling) + '"' + ' ' +
                  'width' + '=' + '"' + str((int(line[0].split(';')[5])-int(line[0].split(';')[3]))*scaling) + '"' + ' ' +
                  'height' + '=' + '"' + str((int(line[0].split(';')[6])-int(line[0].split(';')[4]))*scaling) + '"' + '>' + "\n")

    xml_file.write('      ' + '<' + 'label' + '>' + line[0].split(';')[2] + '<' + '/label' + '>' + '\n')

    xml_file.write('    ' + '<' + '/box' + '>' + '\n')

def convert(csv_path, img_path, scaling):
    print("Converting csv to xml...")
    csvData = csv.reader(open(csv_path))

    xml_ped_path = csv_path[:len(csv_path)-4] + '_ped.xml'
    xml_ped = open(xml_ped_path, 'w')

    xml_mtb_path = csv_path[:len(csv_path)-4] + '_mtb.xml'
    xml_mtb = open(xml_mtb_path, 'w')

    # Write header
    write_header(xml_ped)
    write_header(xml_mtb)

    prev_nr = -1
    first = True
    next(csvData)  # Skip header line
    for line in csvData:
        # tag check
        if(line[0].split(';')[2] == "PED"):
            if(ped_annotation_check(line)):
                write_annotation(line, prev_nr, first, img_path, scaling, xml_ped)
        if(line[0].split(';')[2] == "MTB"):
            if(mtb_annotation_check(line)):
                write_annotation(line, prev_nr, first, img_path, scaling, xml_mtb)
        else:
            print("Unknown tag")

    # Finish file
    xml_ped.close()
    xml_mtb.close()

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
    ap.add_argument("-x", "--xml", type=str,
                    help="Path xml file")
    ap.add_argument("-s", "--scale", type=int,
                    help="Scale factor")
    args = vars(ap.parse_args())

    convert(args["csv"], "4x_44/", args["scale"])
