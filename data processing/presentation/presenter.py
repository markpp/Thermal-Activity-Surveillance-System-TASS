import numpy as np
import cv2
import os
import argparse

import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, color, exposure


def draw_grid(frame, scaling, spacing=10):
    for horizontal in range(spacing, 60, spacing):
        frame = cv2.line(frame, (0, int(horizontal * scaling)), (int(80 * scaling),
                                    int(horizontal * scaling)), (255, 0, 0), 1)

    for vertical in range(spacing, 80, spacing):
        frame = cv2.line(frame, (int(vertical * scaling), 0), (int(vertical * scaling),
                                 int(60 * scaling)), (255, 0, 0), 1)


def draw_rects(frame, frame_number, rects, scaling):
    cv2.putText(frame, str(frame_number), (int(60 * scaling), 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    for rect_index, rect in enumerate(rects):
        #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
        frame = cv2.rectangle(frame, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (255, 255, 0), 1)
    return frame


def draw_detections(frame, frame_number, detections, scaling):
    cv2.putText(frame, str(frame_number), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.25, 255, 1, cv2.LINE_AA)

    for det_index, det in enumerate(detections):
        #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
        frame = cv2.rectangle(frame, (det.x_min, det.y_min), (det.x_max, det.y_max), (255, 255, 0), 1)

    return frame


def draw_tracks(frame, frame_number, tracks, scaling):
    cv2.putText(frame, str(frame_number), (int(60 * scaling), 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    for track_index, track in enumerate(tracks):
        cv2.putText(frame, str(track.det_num), (int(track.p_predict[-1][0]), int(track.p_predict[-1][1])-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(track.track_num), (int(track.p_predict[-1][0]), int(track.p_predict[-1][1]) + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        frame = cv2.rectangle(frame, (track.x_min, track.y_min), (track.x_max, track.y_max), (255, 255, 0), 1)
        center_predict = (int(track.p_predict[-1][0]), int(track.p_predict[-1][1]))
        frame = cv2.circle(frame, center_predict, 6, (255, 255, 0), thickness=1, lineType=8, shift=0)
        center_detect = (int(track.p_detect[-1][0]), int(track.p_detect[-1][1]))
        frame = cv2.circle(frame, center_detect, 4, (255, 255, 0), thickness=1, lineType=8, shift=0)

    return frame


def scale_draw_annotations(frame, frame_number, annotations, scaling = 2.0):
    """Scale frame before preview and draw annotations.

    In order to make it easier to see what is going on, the preview
    frames are scaled before the annotations are added:

    Args:
        frame (np.array): Input frame.
        frame_number (int): Frame number.
        scaling (float): Scaling constant.

    Returns:
        (np.array): Returns scaled frame with annotations.
    """
    frame = cv2.resize(frame, dsize=(0,0), fx=scaling, fy=scaling)
    # draw current frame number to frame
    cv2.putText(frame, str(frame_number), (int(60*scaling), 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    #draw_grid(frame, scaling, 10)
    # Only draw annotation if it exists
    if annotations.has_key(str(frame_number).zfill(6)):
        #for i in range(1, len(annotations[str(frame_number).zfill(6)])):
        #id, x_min, y_min, x_max, y_max = annotations[str(frame_number).zfill(6)]
        for k,v in annotations[str(frame_number).zfill(6)].items():
            tag, x_min, y_min, x_max, y_max = v
            # Bounding box
            frame = cv2.rectangle(frame, (int(x_min*scaling), int(y_min*scaling)),
                     (int(x_max*scaling), int(y_max*scaling)), (255, 255, 0), 1)
            # Start coordinate
            cv2.putText(frame, str(x_min) + "," + str(y_min) + " " + tag, (int(x_min * scaling), int(y_min * scaling)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 1, cv2.LINE_AA)
            # Aspect ratio
            aspect = "{:.2f}".format(float(x_max-x_min)/float(y_max-y_min))
            cv2.putText(frame, str(aspect), (int((x_min + (x_max-x_min)/2) * scaling),
                                             int((y_min + (y_max-y_min)/2) * scaling)),
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


    return frame


def show_hog(frame):
    #frame = color.rgb2gray(data.astronaut())

    fd, hog_image = hog(frame, orientations=8, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualise=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharex=True, sharey=True)

    ax1.axis('off')
    ax1.imshow(frame, cmap=plt.cm.gray)
    ax1.set_title('Input image')
    ax1.set_adjustable('box-forced')

    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
    ax2.set_title('Histogram of Oriented Gradients')
    ax1.set_adjustable('box-forced')
    plt.show()
