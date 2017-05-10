# import the necessary packages
import numpy as np


# Malisiewicz et al.
def non_max_suppression_fast(dets, scores, weights, overlapThresh):
    # if there are no boxes, return an empty list
    if len(dets) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    #if boxes.dtype.kind == "i":
    #    boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    x1 = []
    y1 = []
    x2 = []
    y2 = []

    area = []

    for rect in dets:
        # grab the coordinates of the bounding boxes
        x1.append(float(rect.left()))
        y1.append(float(rect.top()))
        x2.append(float(rect.right()))
        y2.append(float(rect.bottom()))

        # compute the area of the bounding boxes and sort the bounding
        # boxes by the bottom-right y-coordinate of the bounding box
        area.append(rect.area())

    idxs = np.argsort(scores)
    #idxs = idxs[::-1] #  reverse order

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 1:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box

        xx1 = np.maximum(x1[i], x1[idxs[:last][0]])
        yy1 = np.maximum(y1[i], y1[idxs[:last][0]])
        xx2 = np.minimum(x2[i], x2[idxs[:last][0]])
        yy2 = np.minimum(y2[i], y2[idxs[:last][0]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last][0]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type

    output_dets = []
    output_scores = []
    output_weights = []
    for idx in pick:
        output_dets.append(dets[idx])
        output_scores.append(scores[idx])
        output_weights.append(weights[idx])
    return output_dets, output_scores, output_weights
