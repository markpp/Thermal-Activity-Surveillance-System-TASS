import glob
import os
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2

if __name__ == "__main__":
  path = '/media/markpp/WD1TBNTFS/MTBdata/2015-09-02-12-44(27Sep)/'
  #files = glob.glob("/media/markpp/WD1TBNTFS/MTBdata/2015-09-02-12-44(27Sep)/*.png")
  #print files[0]

  
  for filename in os.listdir(path):
    print filename
    imagePath = path + filename
    img = cv2.imread(imagePath,-1)
    
    cv2.imshow('test', img)
    #prefix, num = filename[:-4].split('_')
    
