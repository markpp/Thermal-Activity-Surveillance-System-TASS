"""
Person class.
"""
import filters
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np

class Person:

    def __init__(self, det_num, x_min, y_min, x_max, y_max, score, det_type):
        self.track_num = -1
        self.id = -1
        self.det_num = det_num
        self.det_type = det_type
        self.ped_det_count = 0
        self.mtb_det_count = 0
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

        self.p_detect = []
        self.p_detect.append([x_min + (x_max - x_min) / 2, y_min + (y_max - y_min) / 2])

        self.km = KalmanFilter(dim_x=4, dim_z=2)
        # self.km.x = np.array([self.p_detect[-1][0]], [self.p_detect[-1][1]], [0.], [0.])  # initial state (location and velocity)

        self.km.x = np.array(
            [self.p_detect[-1][0], self.p_detect[-1][1], 0., 0.])  # initial state (location and velocity)

        self.km.F = np.array(
            [[1., 0., 1., 0.], [0., 1., 0., 1.], [0., 0., 1., 0.], [0., 0., 0., 1.], ])  # state transition matrix
        # self.km.F = np.array([[1., 0.], [0., 1.]])  # state transition matrix


        # self.km.H = np.array([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 0., 0.], [0., 0., 0., 0.]])  # Measurement function
        self.km.H = np.array([[1., 0., 0., 0.], [0., 1., 0., 0.]])  # Measurement function

        self.km.P *= 1000.  # covariance matrix
        self.km.R = 5  # state uncertainty
        dt = 0.01
        # self.km.Q = Q_discrete_white_noise(2, dt, .1)  # process uncertainty

        self.p_predict = []
        #print "nu1"
        #self.km_predict()
        #self.km_get_prediction()
        self.p_predict.append(self.p_detect[-1])

        self.score = []
        self.score.append(score)

        self.track_id = -1
        self.skipped_frames = 0
        self.remove_track = False
        self.first_frame = -1

    # Correct coordiante outside of frame
    #def correct_point(coor):

    def km_predict(self):
        self.km.predict()

    def km_get_prediction(self):
        vector = [self.km.x[0], self.km.x[1]]
        self.p_predict.append(vector)
        #print self.p_predict
        #print len(self.p_predict)

    def km_update(self, center):
        #vector = []
        #vector.append(center[0])
        #vector.append(center[1])
        #vector.append(0.2)
        #vector.append(0.1)
        vector = [center[0], center[1]]
        #self.km.update(np.array(vector))
        self.km.update(np.transpose(vector))
