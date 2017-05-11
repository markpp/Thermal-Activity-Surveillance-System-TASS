
import argparse
import csv

def read_detections(anno_path):
    """Read csv file with annotations into dictionary structure.

    The csv annotation file is parsed line by line and annotations are
    stored in dictionary with frame number as key:

    Args:
        anno_path (str): Path to csv file.

    Returns:
        (dict): Returns dictionary of annotations.
    """
    time_stamps = []
    annotations = {}
    prev_nr = -1
    print "Reading annotations..."
    # read annotations line by line from file
    with open(anno_path) as anno_file:
        next(anno_file)  # Skip header line
        for line in anno_file:
            frame_nr, det_type, score, left, top, height, width = line.split(';')
            print(frame_nr)


    #with open('/Users/markpp/Desktop/test_ped.csv', 'wb') as fp:
    #     a = csv.writer(fp, delimiter='\n')
    #    a.writerow(time_stamps)




if __name__ == "__main__":
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:

    -p /Users/markpp/Desktop/code/data/2015-09-28-12-39 -a /Users/markpp/Desktop/code/my_repos/MTB/data/annotations/2015-09-28-12-39_anno.csv -f 4890
    """

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--detections", type=str,
                    help="Path to frames")
    args = vars(ap.parse_args())

    # Prepare path to frames
    csv_path = args["detections"]
    read_detections(csv_path)
