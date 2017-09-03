import numpy as np
import persons
import csv
import tracking
from munkres import Munkres

class Tracker:

    def __init__(self):
        self.track_id = 0
        self.tracks = []
        self.assignments = []
        self.cost_thres = 200.0 #90
        self.max_skipped_frames = 15
        self.unassigned_dets = []
        self.unassigned_tracks = []
        

    def update(self, dets, frame_num):
        """Update tracks.

        Matches detections and tracks:

        Args:
            dets (person[]): List of detected persons.
            frame_num (int): Frame number.

        """

        self.assignments = []
        self.unassigned_dets = []
        track_num = 0
        # Create new tracks
        if len(self.tracks) is 0:
            if __debug__:
                print "Create new tracks"
            for det in dets:
                det.first_frame = frame_num
                det.id = self.track_id
                det.track_num = track_num
                track_num = +1
                self.track_id = +1
                self.tracks.append(det)

        # Define cost Matrix
        N = len(self.tracks) # Number of existing tracks
        M = len(dets) # Number of detections to assign

        if __debug__:   
            print "Num dets: {} num tracks: {}".format(M, N)
        # Calculate cost
        # Make cost mat square
        '''
        if M > N:
            N = M
        elif M < N:
            M = N
        '''

        #cost_mat[assign_index][assign_index] == 0
        cost_mat = np.zeros((N,M))
        #cost_mat = np.ones((N,M))*40.0
        for row_index, track in enumerate(self.tracks):
            for col_index, det in enumerate(dets):
                # stores the cost - ecludian distance between the two points
                #print track.p_predict
                ecludian_dist = np.linalg.norm(np.array(track.p_predict[-1]) - np.array(det.p_detect[-1]))
                #print ecludian_dist
                cost_mat[row_index][col_index] = ecludian_dist

        #cost_mat = cost_mat[::-1,:]
        #print "cost mat shape: {}".format(np.array(cost_mat).shape)
        #print cost_mat

        # Solve assignment
        if len(self.tracks) > 0:
            #m = Munkres()
            #indexes = m.compute(cost_mat)
            #lst1, lst2 = zip(*indexes)
            #self.assignments = list(lst2)

            #self.assignments = tracking.dlib_hungarian.assignment_dlib(cost_mat)

            my_hungarian = tracking.hungarian.Hungarian(np.transpose(cost_mat))
            my_hungarian.calculate()
            result = my_hungarian.get_results()
            if __debug__:
                print("result: {}".format(result))
            
            if result:
                lst1, lst2 = zip(*result)
                self.assignments = list(lst1)
            else:
                self.assignments = [-1]

        #print self.assignments
        # Clean bad assignments
        assign_index = 0
        while assign_index < len(self.assignments):
            if self.assignments[assign_index] != -1:
                if __debug__:
                    print("lowest cost: {}").format(min(cost_mat[assign_index][:]))
                if min(cost_mat[assign_index][:]) > self.cost_thres:
                    self.assignments[assign_index] = -1
                    # mark as unassigned
                    self.unassigned_tracks.append(assign_index)
            else:
                if __debug__:
                    print "skipped_frames + 1"
                self.tracks[assign_index].skipped_frames += 1
            assign_index += 1
        '''
        # Clean bad assignments
        for assign_index, assign in enumerate(self.assignments):
            if assign != -1:
                if cost_mat[assign_index][assign] > self.cost_thres:
                    assign = -1
                    # mark as unassigned
                    self.unassigned_tracks.append(assign_index)

            else:
                #print "ups"
                self.tracks[assign_index].skipped_frames = +1

        mylist = []
        for e in self.assignments:
            mylist.append(int(e))
        print mylist
        '''
        if __debug__:    
            print self.assignments
        # Search for unassigned detections
        for det_index, det in enumerate(dets):
            if int(det_index) not in self.assignments:
                #print "det_index not in list: " +str(det_index)
                self.unassigned_dets.append(det)
            #else:
                #print "det_index is in list: " +str(det_index)

        # Start new tracks for unassigned detections
        if len(self.unassigned_dets) > 0:
            if __debug__:
                print "Start new tracks for unassigned detections"
            for det in self.unassigned_dets:
                det.first_frame = frame_num
                det.id = self.track_id
                self.track_id += 1
                self.tracks.append(det)

        # Update Kalman...
        #print "Assingment length: " + str(len(self.assignments))
        #print "Track length: " + str(len(self.tracks))
        for assign_index, assign in enumerate(self.assignments):
            #print "assign_index: " + str(assign_index)

            self.tracks[assign_index].km_predict()
            #print "last prediction: " + str(self.tracks[assign_index].p_predict[-1])
            # if detection has been assigned
            if assign != -1:
                self.tracks[assign_index].skipped_frames = 0
                # Add newest detection to track
                self.tracks[assign_index].p_detect.append(dets[assign_index].p_detect[-1])

                # Update bounding box
                self.tracks[assign_index].x_min = dets[assign_index].x_min
                self.tracks[assign_index].y_min = dets[assign_index].y_min
                self.tracks[assign_index].x_max = dets[assign_index].x_max
                self.tracks[assign_index].y_max = dets[assign_index].y_max
                
                if dets[assign_index].det_type == 1:
                    self.tracks[assign_index].ped_det_count += 1
                else:
                    self.tracks[assign_index].mtb_det_count += 1                                

                # Predict next location based on newest detection
                self.tracks[assign_index].km_update(dets[assign_index].p_detect[-1])
                self.tracks[assign_index].km_get_prediction()
                #self.tracks[assign_index].p_predict.append([track.p_predict[-1][0], track.p_predict[-1][1]])
            else:
                # Predict next location based xx
                #self.tracks[assign_index].kalman_filter.km_update([0, 0])
                #self.tracks[assign_index].km_predict()
                self.tracks[assign_index].km_get_prediction()
                #self.tracks[assign_index].p_predict.append()

            # Clean trace history
            # TODO

            self.tracks[assign_index].lifetime =+ 1

        # Remove tracks with not detections after max_skipped_frames
        for track in self.tracks:
            track.remove_track = False
            if track.skipped_frames > self.max_skipped_frames:
                track.remove_track = True
                if __debug__:
                    print("track {} has died".format(track.track_id))
                
                type_tag = 'B'
                if track.mtb_det_count < track.ped_det_count:
                    type_tag = 'P'
                    
                with open('../data/tracks/tracks.csv', 'a') as csvfile:
                    track_writer = csv.writer(csvfile, delimiter=';')
                    track_writer.writerow([frame_num, type_tag, '\n'])
                # Look at the track and determine what it was
                # TODO

            # Check if track moved out side of frame and remove

            #if(track.remove_track == True):
        if __debug__:
            print("Track length: {}".format(len(self.tracks)))
            
        self.tracks = [x for x in self.tracks if not x.remove_track]
        
        if __debug__:
            print("Track length after cleanup: {}".format(len(self.tracks)))
