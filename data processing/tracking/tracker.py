import numpy as np
import persons
import tracking
from munkres import Munkres

from sort import *


class Tracker:

    def __init__(self):
        # create instance of SORT
        self.mot_tracker = Sort()
        self.track_bbs_ids = []

    def update(self, dets):
        '''
        input:
        [[x,y,w,h,score],[x,y,w,h,score],...]

        output:
        [[x,y,w,h,object ID],[x,y,w,h,object ID],...]
        '''
        # update SORT
        self.track_bbs_ids = self.mot_tracker.update(dets)
        print self.track_bbs_ids
        # track_bbs_ids is a np array where each row contains
        # a valid bounding box and track_id (last column)
