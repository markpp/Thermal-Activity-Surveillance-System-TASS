import numpy as np
import cv2

import csv
import time
import tools
import presentation
import detection
import tracking
import persons


# Process frames continously or step through
def detect_hog(frames_dir, start_frame, frame_list):
    """runs detector and prints the properties of each detection to file.

    """
    hog_detector = detection.fhog_detector.detector()
    hog_detector.load_dlib_detector()

    index = 0
    with open('../data/tracks/log.csv', 'wb') as csvfile:
        track_writer = csv.writer(csvfile, delimiter=';')
        # track_writer.writerow(['frame_nr', 'type', 'score', 'left', 'top', 'height', 'width'])
        track_writer.writerow(['frame_nr', 'type', 'score', 'center_x', 'center_y'])

        while index < len(frame_list):
            # print("frame_list[-1]: {}".format(frame_list[-1]))
            # print("index: {}".format(index))
            # print("frame_list[index]: {}".format(frame_list[index]))
            frame_nr = frame_list[index]
            if int(frame_nr) < start_frame:
                index = index+1
            else:
                frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
                frame = cv2.imread(frame_path, -1)
                if frame is not None:
                    #img = np.clip(img, 0, 8191)
                    #img = np.array(img / 4).astype(np.uint8)
                    #frame = img
                    #frame = cv2.resize(img, dsize=(0, 0), fx=4.0, fy=4.0)

                    rects, scores, det_types = hog_detector.execute_dlib_detector(frame)
                    detections = []
                    for det_num, (rect, score, det_type) in enumerate(zip(rects, scores, det_types)):
                        #print(str(rect.left()) + " " + str(score)
                        current_det = persons.person.Person(det_num, rect.left(), rect.top(), rect.right(), rect.bottom(), score, det_type)

                        detections.append(current_det)
                        # Write detection properties to file
                        # frame_nr, trajectory_id(-1 for detections), x_min, y_min, width, height, score, -1, -1

                        # Sort tracks

                        track_writer.writerow([int(frame_nr), int(det_type), score, int(rect.center().x), int(rect.center().y)])
                        #print("frame_nr: {:d}; type: {:d}; score: {:0.2f}; center_x: {:d}; center_y: {:d}; height: {:d}; width: {:d}".format(int(frame_nr), int(det_type), score, rect.left()+rect.width()/2, rect.top()+rect.height()/2, rect.height(), rect.width()))

                    cv2.imshow('Preview', presentation.presenter.draw_detections(frame, frame_nr, detections, 4.0))
                else:
                    print('read failed for: ')
                    print(frame_path)
                # For continous processing

                # For stepping through
                k = cv2.waitKey(20)
                if k == ord('b'):
                    index = index - 1
                    #print("Next frame <- {}".format(int(frame_nr) - 1))
                elif k == ord('q'):
                    print("Quitting...")
                    break
                elif k == ord('p'):
                    print("Paused.")
                    cv2.waitKey()
                    print("Unpaused.")
                else:
                    index = index + 1
                    #print("Next frame -> {}".format(int(frame_nr) + 1))


def detect_hog_tracked(frames_dir, start_frame, frame_list):
    """runs detector and prints the properties of each detection to file.

    """
    hog_detector = detection.fhog_detector.detector()
    hog_detector.load_dlib_detector()

    # Initialize tracker
    mtb_tracker = tracking.tracker.Tracker()

    index = 0
    with open('../data/tracks/dets.csv', 'wb') as csvfile:
        track_writer = csv.writer(csvfile, delimiter=';')
        track_writer.writerow(['frame_nr', 'type', 'score', 'left', 'top', 'right', 'bottom'])

        while index < len(frame_list):
            frame_nr = frame_list[index]
            if int(frame_nr) < start_frame:
                index = index+1
            else:
                frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
                frame = cv2.imread(frame_path, -1)
                if frame is not None:
                    #import time
                    #start_time = time.time()

                    rects, scores, det_types = hog_detector.execute_dlib_detector(frame)
                    detections = []
                    for det_num, (rect, score, det_type) in enumerate(zip(rects, scores, det_types)):
                        #print(str(rect.left()) + " " + str(score)
                        current_det = persons.person.Person(det_num, rect.left(), rect.top(), rect.right(), rect.bottom(), score, det_type)

                        detections.append(current_det)

                        track_writer.writerow([int(frame_nr), int(det_type), "{:.4f}".format(score), int(rect.left()), int(rect.top()), int(rect.right()), int(rect.bottom())])

                    # Update tracker with new detections
                    #detections.append([7.0, 7.0, 59.0, 88.0])
                    #print(detections)
                    mtb_tracker.update(detections, frame_nr, debug=False)

                    #print("%s" % (time.time() - start_time))
                    #cv2.imshow('Preview', presentation.presenter.draw_tracks(frame, frame_nr, mtb_tracker.track_bbs_ids, 4.0))
                    cv2.imshow('Preview', presentation.presenter.draw_tracks(frame, frame_nr, mtb_tracker.tracks, 4.0))
                else:
                    print('read failed for: ')
                    print(frame_path)
                # For continous processing
                #k = 32
                #cv2.waitKey(30)
                # For stepping through
                k = cv2.waitKey(30)
                if k == ord('b'):
                    index = index - 1
                elif k == ord('q'):
                    print("Quitting...")
                    break
                elif k == ord('p'):
                    print("Paused.")
                    cv2.waitKey()
                    print("Unpaused.")
                else:
                    index = index + 1


# Process only frames with annotated objects
def detect_hog_tracked_anno(frames_dir, annotations):

    mtb_tracker = tracking.tracker.Tracker()

    hog_detector = detection.fhog_detector.detector()
    hog_detector.load_dlib_detector()
    frame_list = sorted(annotations)
    # Sort the unordered dictionary and used the sorted keys to find relevant frames
    index = 0
    #for frame_nr in sorted(annotations):
    while index < len(frame_list):
        frame_nr = frame_list[index]
        if int(frame_nr) < start_frame:
            index = index+1
        else:
            #print("%s: %s" % (frame_nr, annotations[frame_nr])
            frame_path = frames_dir + '/frame_' + str(frame_nr).zfill(6) + '.png'
            # print(frame_path
            frame = cv2.imread(frame_path, -1)
            if frame is not None:

                #img2 = cv2.imread("/Users/markpp/Desktop/code/VAPprojects/PythonHoG/bikes/images8x/frame_004297.png", -1)
                #presentation.presenter.show_hog(frame)
                #cv2.imshow('Preview', presentation.presenter.scale_draw_annotations(img, frame_nr, annotations, 4.0))
                detections = []
                rects, scores = hog_detector.execute_dlib_detector(frame)
                for det_num, (rect, score) in enumerate(zip(rects, scores)):
                    #print(str(rect.left()) + " " + str(score)
                    current_det = persons.person.Person(det_num, rect.left(), rect.top(), rect.right(), rect.bottom(), score)
                    detections.append(current_det)

                mtb_tracker.update(detections, frame_nr)
                #print("Number of tracks: " + str(len(mtb_tracker.tracks))
                #cv2.imshow('Preview', presentation.presenter.draw_detections(frame, frame_nr, detections, 4.0))

                cv2.imshow('Preview', presentation.presenter.draw_tracks(frame, frame_nr, mtb_tracker.tracks, 4.0))

            else:
                print('read failed for: ')
                print(frame_path)
            # cv2.waitKey()
            k = cv2.waitKey()
            # print(k
            if k == 32:
                index = index + 1
                print("Next frame -> {}".format(int(frame_nr) + 1))
            if k == ord('b'):
                index = index - 1
                print("Next frame <- {}".format(int(frame_nr) - 1))
            elif k == ord('q'):
                print("Quitting...")

                break
            elif k == ord('p'):
                print("Paused.")
                cv2.waitKey()
                print("Unpaused.")
    mtb_tracker.close()

def train_detector():

    hog_detector = detection.fhog_detector.detector()
    hog_detector.train_dlib_detector()
    hog_detector.load_dlib_detector()
    #hog_detector.show_learned_hog_filter()
    hog_detector.evaluate_dlib_detector()
