
import cv2


def store_frame(frame, frame_nr, scale, output_dir):
    frame_path = output_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
    #print frame_path
    frame = cv2.resize(frame, dsize=(0, 0), fx=scale, fy=scale)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(frame_path, frame)


def read_annotations(anno_path):
    """Read csv file with annotations into dictionary structure.

    The csv annotation file is parsed line by line and annotations are
    stored in dictionary with frame number as key:

    Args:
        anno_path (str): Path to csv file.

    Returns:
        (dict): Returns dictionary of annotations.
    """

    annotations = {}
    prev_nr = -1
    print("Reading annotations...")
    # read annotations line by line from file
    with open(anno_path) as anno_file:
        next(anno_file) # Skip header line
        for line in anno_file:
            #print line
            frame_nr = line.split('_')[1].split('.')[0]
            if int(frame_nr != prev_nr):
                annotations[str(frame_nr)] = {}
                prev_nr = frame_nr
            # Keys:                  frame number                      object id
            annotations[str(line.split('_')[1].split('.')[0])][str(line.split(';')[1])] = \
                       [str(line.split(';')[2]), # tag
                        int(line.split(';')[3]), # x min
                        int(line.split(';')[4]), # y min
                        int(line.split(';')[5]), # x max
                        int(line.split(';')[6])] # y max

    return annotations
