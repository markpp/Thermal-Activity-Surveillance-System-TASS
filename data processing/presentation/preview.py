import numpy as np
import cv2

import tools
import presentation


def continous_preview(frames_dir, annotations):
    # Consecutive preview of frames
    frame_nr_begin = args["frame"]
    for frame_nr in range(frame_nr_begin, frame_nr_begin + 1000):
        # for index in range(frameNumber, len(os.listdir(path))):
        frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
        # print frame_path
        img = cv2.imread(frame_path, -1)
        if img is not None:
            img = np.clip(img, 0, 8191)
            img = np.array(img / 4).astype(np.uint8)
            cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, 4.0))
        else:
            print 'read failed for: '
            print frame_path
        # cv2.waitKey()
        k = cv2.waitKey(33)
        if k == ord('q'):
            print "Quitting..."
            break
        elif k == ord('p'):
            print "Paused."
            cv2.waitKey()
            print "Unpaused."


def annotation_preview(frames_dir, annotations, start_frame):
    # Showing only frames with annotated objects

    frame_list = sorted(annotations)
    output_dir = "../data/training/4x"
    # Sort the unordered dictionary and used the sorted keys to find relevant frames
    #for frame_nr in sorted(annotations):
    #for frame_nr in frame_list:
    index = 0
    while index < len(frame_list):
        frame_nr = frame_list[index]
        if int(frame_nr) < start_frame:
            index = index+1
        else:
            #print "%s: %s" % (frame_nr, annotations[frame_nr])
            frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
            # print frame_path
            img = cv2.imread(frame_path, -1)
            if img is not None:
                img = np.clip(img, 0, 8191)
                img = np.array(img / 4).astype(np.uint8)
                tools.file_handler.store_frame(img, frame_nr, 4.0, output_dir)
                cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, 4.0))
            else:
                print 'read failed for: '
                print frame_path

            k = cv2.waitKey(20)
            #print k
            if k == 32:
                index = index+1
                print "Next frame -> {}".format(int(frame_nr)+1)
            if k == ord('b'):
                index = index-1
                print "Next frame <- {}".format(int(frame_nr)-1)
            elif k == ord('q'):
                print "Quitting..."
                break
            elif k == ord('p'):
                print "Paused."
                cv2.waitKey()
                print "Unpaused."
            else:
                index = index + 1
                print "Next frame -> {}".format(int(frame_nr) + 1)
