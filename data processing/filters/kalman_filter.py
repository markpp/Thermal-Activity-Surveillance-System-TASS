"""
Kalman class.
"""
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

class Kalman:

    def __init__(self, x_min, y_min, x_max, y_max, score):
        self.my_filter = my_filter = KalmanFilter(dim_x=4, dim_z=2)
