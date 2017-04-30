"""
Sample script to convert an csv annotation file into a xml file.
"""

import csv
import os
import argparse


def mtb_annotation_check(annotation):

    # tag check
    if(annotation[0].split(';')[2] != "MTB"):
        return False

    # width check
    width = int(annotation[0].split(';')[5])-int(annotation[0].split(';')[3])
    if(width < 10):
        print "Annotation: {}, failed width check - {}".format(annotation[0].split(';')[0], width)
        return False

    # height check
    height = int(annotation[0].split(';')[6])-int(annotation[0].split(';')[4])
    if(height < 10):
        print "Annotation: {}, failed height check - {}".format(annotation[0].split(';')[0], height)
        return False

    # aspect ratio check
    ratio = float(width)/float(height)
    if(ratio >= 0.5 and ratio <= 1.0): # MTB
        return True
    else:
        print "Annotation: {}, failed ratio check - {}".format(annotation[0].split(';')[0], ratio)
        return False


def ped_annotation_check(annotation):

    # tag check
    if(annotation[0].split(';')[2] != "PED"):
        return False

    # width check
    width = int(annotation[0].split(';')[5])-int(annotation[0].split(';')[3])
    if(width < 5):
        print "Annotation: {}, failed width check - {}".format(annotation[0].split(';')[0], width)
        return False

    # height check
    height = int(annotation[0].split(';')[6])-int(annotation[0].split(';')[4])
    if(height < 10):
        print "Annotation: {}, failed height check - {}".format(annotation[0].split(';')[0], height)
        return False

    # aspect ratio check
    ratio = float(width)/float(height)
    if(ratio < 0.55): # PED
        return True
    else:
        print "Annotation: {}, failed ratio check - {}".format(annotation[0].split(';')[0], ratio)
        return False


def convert(csv_path, xml_path, scaling):
    print "Converting csv to xml..."
    csvData = csv.reader(open(csv_path))
    xmlData = open(xml_path, 'w')
    xmlData.write('<?xml version="1.0" encoding="ISO-8859-1"?>' + "\n")
    xmlData.write('<?xml-stylesheet type="text/xsl" href="image_metadata_stylesheet.xsl"?>' + "\n")
    xmlData.write('<dataset>' + "\n")
    xmlData.write('<name>Training faces</name>' + "\n")
    xmlData.write('<comment>These are images from my thermal MTB dataset.</comment>' + "\n")
    xmlData.write('<images>' + '\n')
    prev_nr = -1
    first = True
    next(csvData)  # Skip header line
    for line in csvData:
        #if(mtb_annotation_check(line)):
        if(ped_annotation_check(line)):
            frame_nr = line[0].split('_')[1].split('.')[0]
            #print frame_nr
            if frame_nr != prev_nr:
                if not first:
                    xmlData.write('  ' + '<' + '/image' + '>' + "\n")
                first = False

                xmlData.write('  ' + '<' + 'image' + ' ' + 'file' + '=' + '"' + "4x/" + line[0].split(';')[0] + '"' + '>' + "\n")
                prev_nr = frame_nr

            xmlData.write('    ' + '<' + 'box' + ' ' + 'top' + '=' + '"' + str(int(line[0].split(';')[4])*scaling) + '"' + ' ' +
                          'left' + '=' + '"' + str(int(line[0].split(';')[3])*scaling) + '"' + ' ' +
                          'width' + '=' + '"' + str((int(line[0].split(';')[5])-int(line[0].split(';')[3]))*scaling) + '"' + ' ' +
                          'height' + '=' + '"' + str((int(line[0].split(';')[6])-int(line[0].split(';')[4]))*scaling) + '"' + '>' + "\n")

            xmlData.write('      ' + '<' + 'label' + '>' + line[0].split(';')[2] + '<' + '/label' + '>' + '\n')

            xmlData.write('    ' + '<' + '/box' + '>' + '\n')

    xmlData.write('  ' + '<' + '/image' + '>' + "\n")
    xmlData.write('</images>' + "\n")
    xmlData.write('</dataset>' + "\n")
    xmlData.close()

if __name__ == '__main__':
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    python csv2xml.py -c /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.csv -x /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.xml -s 4
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

    convert(args["csv"], args["xml"], args["scale"])
