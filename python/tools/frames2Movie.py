import glob
import os
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
import scipy
import sys

if __name__ == "__main__":
  path = sys.argv[1]
  #path = '/home/markpp/Desktop/dataMTB/input/2015-09-02-12-44/'
  #files = glob.glob("/media/markpp/WD1TBNTFS/MTBdata/2015-09-02-12-44(27Sep)/*.png")
  #print files[0]
  imagePath = ""
  #fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
  fourcc = cv2.VideoWriter_fourcc(*'MJPG')
  videoOut = cv2.VideoWriter('2015-09-30-06-23.avi',fourcc, 9, (80,60), False)
  #print len(os.listdir(path))
  imageCount = len(os.listdir(path))
  for frame in range(0,imageCount):
    filename = 'frame_' + str(frame).zfill(6) + '.png'
    imagePath = path + filename
    #print imagePath
    img = cv2.imread(imagePath,-1)
    #if(img.size == 0):
      #break
    #img = (img/4).astype(np.uint8)
    #np.bitwise_and(img, 1023)
    if(hasattr(img, 'astype')):
      oldImg = img    
    else:
      print 'not image'
      print imagePath
      if(frame < imageCount):
        img = oldImg
        cv2.imwrite(imagePath, img)
      else:
        break

    img = np.clip(img, 0, 8191)
    img = (img/4).astype(np.uint8)
    #cv2.imshow('test', img)
    videoOut.write(img)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
      #break
  
  videoOut.release()
    #prefix, num = filename[:-4].split('_')
    
