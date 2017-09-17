"""
Sample script to convert an csv annotation file into a xml file.
"""

import csv
import os
import argparse

def mtb_annotation_check(annotation, scale):
    # width check
    width = int(annotation[0].split(';')[5])-int(annotation[0].split(';')[3])
    if(width < 8*scale):
        print("Annotation: {}, failed width check - {}".format(annotation[0].split(';')[0], width))
        return False

    # height check
    height = int(annotation[0].split(';')[6])-int(annotation[0].split(';')[4])
    if(height < 10*scale):
        print("Annotation: {}, failed height check - {}".format(annotation[0].split(';')[0], height))
        return False

    # area check
    area = height*width*scale*scale
    if(area < 400):
        print("Annotation: {}, failed area check - {}".format(annotation[0].split(';')[0], area))
        return False

    # aspect ratio check
    ratio = float(height)/float(width)
    if(ratio > 1.1 and ratio < 1.7): # MTB
        return True
    else:
        print("Annotation: {}, failed ratio check - {}".format(annotation[0].split(';')[0], ratio))
        return False

def ped_annotation_check(annotation, scale):
    # width check
    width = int(annotation[0].split(';')[5])-int(annotation[0].split(';')[3])
    if(width < 8*scale):
        print("Annotation: {}, failed width check - {}".format(annotation[0].split(';')[0], width))
        return False

    # height check
    height = int(annotation[0].split(';')[6])-int(annotation[0].split(';')[4])
    if(height < 12*scale):
        print("Annotation: {}, failed height check - {}".format(annotation[0].split(';')[0], height))
        return False

    # area check
    area = height*width*scale*scale
    if(area < 400):
        print("Annotation: {}, failed area check - {}".format(annotation[0].split(';')[0], area))
        return False

    # aspect ratio check
    ratio = float(height)/float(width)
    if(ratio > 1.8 and ratio < 2.6): # PED
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

def write_annotation(line, prev_nr, img_path, scaling, xml_file, first_annotation):
    frame_name = line[0].split(';')[0]
    frame_nr = int(line[0].split('_')[1].split('.')[0])
    label = line[0].split(';')[2]
    x_min = int(line[0].split(';')[3])
    x_max = int(line[0].split(';')[5])
    y_min = int(line[0].split(';')[4])
    y_max = int(line[0].split(';')[6])


    if frame_nr != prev_nr: # If new frame, end previous image entry and add new beginning to next image entry
        if not first_annotation: # Add end to previous image entry, except if this is the first annotation
            xml_file.write('  ' + '<' + '/image' + '>' + "\n")
        first_annotation = False # Set to false at first run

        xml_file.write('  ' + '<' + 'image' + ' ' + 'file' + '=' + '"' + img_path + '/' + frame_name + '"' + '>' + "\n")

    xml_file.write('    ' + '<' + 'box' + ' ' +
                   'top' + '=' + '"' + str(y_min*scaling) + '"' + ' ' +
                   'left' + '=' + '"' + str(x_min*scaling) + '"' + ' ' +
                   'width' + '=' + '"' + str((x_max-x_min)*scaling) + '"' + ' ' +
                   #'height' + '=' + '"' + str((y_max-y_min)*scaling) + '"' + '>' + "\n")
                   'height' + '=' + '"' + str((y_max-y_min)*scaling) + '"' + '/>' + "\n")

    #xml_file.write('      ' + '<' + 'label' + '>' + label + '<' + '/label' + '>' + '\n')
    #xml_file.write('    ' + '<' + '/box' + '>' + '\n')

    return frame_nr, first_annotation

def convert(csv_path, img_path, scaling):
    print("Converting csv to xml...")
    csvData = csv.reader(open(csv_path))

    xml_all_path = csv_path[:len(csv_path)-17] + '_all.xml'
    xml_all = open(xml_all_path, 'w')

    xml_ped_path = csv_path[:len(csv_path)-17] + '_ped.xml'
    xml_ped = open(xml_ped_path, 'w')

    xml_mtb_path = csv_path[:len(csv_path)-17] + '_mtb.xml'
    xml_mtb = open(xml_mtb_path, 'w')

    first_annotation_all = True
    first_annotation_ped = True
    first_annotation_mtb = True
    # Write header
    write_header(xml_all)
    write_header(xml_ped)
    write_header(xml_mtb)

    prev_nr = -1
    prev_nr_all = -1
    next(csvData)  # Skip header line
    for line in csvData:
        # tag check
        tag = line[0].split(';')[2]
        if(tag == "PED" or tag == "MTB"):
            prev_nr_all, first_annotation_all = write_annotation(line, prev_nr_all, img_path, scaling, xml_all, first_annotation_all)
        else:
            print("Unknown tag: {}".format(tag))
            print("Line: {}".format(line))

        if(tag == "PED"):
            if(ped_annotation_check(line,2)):
                prev_nr, first_annotation_ped = write_annotation(line, prev_nr, img_path, scaling, xml_ped, first_annotation_ped)
        if(tag == "MTB"):
            if(mtb_annotation_check(line,2)):
                prev_nr, first_annotation_mtb = write_annotation(line, prev_nr, img_path, scaling, xml_mtb, first_annotation_mtb)


    # Write header
    write_footer(xml_all)
    write_footer(xml_ped)
    write_footer(xml_mtb)

    # Finish file
    xml_all.close()
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
    ap.add_argument("-p", "--path", type=str,
                    help="Path to image files")
    ap.add_argument("-s", "--scale", type=int,
                    help="Scale factor")
    args = vars(ap.parse_args())

    convert(args["csv"], args["path"], args["scale"])
