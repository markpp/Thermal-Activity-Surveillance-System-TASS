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
    #prefix, num = filename[:-4].split('_')
    num, postfix = filename[:].split('.')
    num = num.zfill(6)
    if(postfix == 'png'):
      new_filename = "frame_" + num + ".png"
      print new_filename
      os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
  #with open('sunday.csv', 'rb') as f:
    #reader = csv.reader(f)
    #mylist = list(reader)

    #img = cv2.imread('messi5.jpg',-1)

	#for line in open('sunday.csv', 'r'):

