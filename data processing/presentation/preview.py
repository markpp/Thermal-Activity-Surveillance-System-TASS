import numpy as np
import cv2

import tools
import presentation


def continous_preview(frame_nr, frames_dir, annotations, scaling_factor):
    # Consecutive preview of frames
    frame_nr_begin = frame_nr
    for frame_nr in range(frame_nr_begin, frame_nr_begin + 100000):
        # for index in range(frameNumber, len(os.listdir(path))):
        frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
        # print(frame_path
        img = cv2.imread(frame_path, -1)
        if img is not None:
            img = np.clip(img, 0, 8191)
            img = np.array(img / 4).astype(np.uint8)
            cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, scaling_factor))
        else:
            print('read failed for: ')
            print(frame_path)

        k = cv2.waitKey(33)
        if k == ord('q'):
            print("Quitting...")
            break
        elif k == ord('p'):
            print("Paused.")
            cv2.waitKey()
            print("Unpaused.")


def annotation_preview(frames_dir, annotations, start_frame, scaling_factor):
    # Showing only frames with annotated objects

    frame_list = sorted(annotations)
    output_dir = "../data/training/" + str(scaling_factor) + "x/"

    index = 0
    while index < len(frame_list):
        frame_nr = frame_list[index]
        if int(frame_nr) < start_frame:
            index = index+1
        else:
            frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
            img = cv2.imread(frame_path, -1)
            if img is not None:
                cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, scaling_factor))
            else:
                print('read failed for: ')
                print(frame_path)

            k = cv2.waitKey(20)
            if k == ord('b'):
                index = index-1
            elif k == ord('q'):
                print("Quitting...")
                break
            elif k == ord('p'):
                print("Paused.")
                cv2.waitKey()
                print("Unpaused.")
            else:
                index = index + 1
                print("Next frame -> {}".format(int(frame_nr) + 1))


def track_preview(frames_dir, track_path, start_frame, scaling_factor):
    # Showing only frames with annotated objects
    exit = False
    begin_offset = -30
    with open(track_path) as track_file:
        for line in track_file:
            if(exit):
                break
            #print line
            frame_nr = int(line.split(';')[0])

            org_frame_nr = frame_nr
            if(frame_nr < start_frame):
                continue
            if(frame_nr+begin_offset > 0):
                frame_nr = frame_nr+begin_offset
            else:
                frame_nr = 0
            initial_frame_nr = frame_nr
            print("new track at {}".format(org_frame_nr))
            while frame_nr < initial_frame_nr+30:
                frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
                img = cv2.imread(frame_path, -1)
                if img is not None:
                    cv2.imshow('Preview', presentation.presenter.scale_present(img, frame_nr, scaling_factor))
                else:
                    print('read failed for: ')
                    print(frame_path)

                k = cv2.waitKey(20)
                if k == ord('b'):
                    frame_nr = frame_nr-1
                elif k == ord('q'):
                    print("Quitting...")
                    exit = True
                    break
                elif k == ord('p'):
                    print("Paused.")
                    cv2.waitKey()
                    print("Unpaused.")
                else:
                    frame_nr = frame_nr + 1
