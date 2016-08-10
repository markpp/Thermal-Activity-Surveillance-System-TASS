import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
import scipy
import sys

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]


def check_opencv_version(major):
    # return whether or not the current OpenCV version matches the
    # major version number
    return cv2.__version__.startswith(major)
    
    
if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("-p", "--path", type=str,
                  help="Path to frames")
  ap.add_argument("-v", "--video", type=str, default="../../data/new_vid.avi",
                  help="(optional) name of output video file")
  args = vars(ap.parse_args())

  path = args["path"]

  imagePath = ""

  # OpenCV 3.x
  if(check_opencv_version("3.")):
      fourcc = cv2.VideoWriter_fourcc(*'MJPG')
      #fourcc = cv2.VideoWriter_fourcc(*'XVID')
      #fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
  # OpenCV 2.x
  else:
       fourcc = cv2.cv.CV_FOURCC(*'MJPG')
       #fourcc = cv2.cv.CV_FOURCC(*'XVID')
       
  videoOut = cv2.VideoWriter(args["video"],fourcc, 9, (80,60), False)
  imageCount = len(mylistdir(path))
  print imageCount
  for frame in range(0,imageCount):
    filename = '/frame_' + str(frame).zfill(6) + '.png'
    imagePath = path + filename
    img = cv2.imread(imagePath,-1)
    if(hasattr(img, 'astype')):
      oldImg = img    
    else:
      print 'not image'
      print imagePath
      if(frame < imageCount):
        img = oldImg
        #cv2.imwrite(imagePath, img)
      else:
        break
    img = np.clip(img, 0, 8191)
    img = (img/4).astype(np.uint8)
    videoOut.write(img)
    #cv2.imshow('test', img)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
      #break
  
  videoOut.release()

