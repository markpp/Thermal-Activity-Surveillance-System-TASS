#!/usr/bin/env python

import os, sys
import datetime
import numpy as np
import cv2

from pylepton import Lepton

def capture(flip_v = False, device = "/dev/spidev0.0"):

  with Lepton(device) as l:
    a,s = l.capture()
  if flip_v:
    cv2.flip(a,-1,a) #a flag to specify how to flip the array; 0 means flipping around the x-axis and positive value (for example, 1) means flipping around y-axis. Negative value (for example, -1) means flipping around both axes.
  return a,s

if __name__ == '__main__':
  from optparse import OptionParser

  usage = "usage: %prog [options] output_file[.format]"
  parser = OptionParser(usage=usage)

  parser.add_option("-f", "--flip-vertical",
                    action="store_true", dest="flip_v", default=1,
                    help="flip the output image vertically")

  parser.add_option("-d", "--device",
                    dest="device", default="/dev/spidev0.1",
                    help="specify the spi device node (might be /dev/spidev0.1 on a newer device)")

  (options, args) = parser.parse_args()

  #if len(args) < 1:
    #print "You must specify an output filename"
    #sys.exit(1) 
  now = datetime.datetime.now()
  timeNowString = now.strftime('%Y-%m-%d-%H-%M')
  print "Start time: " + timeNowString

  
  sum = -1
  lastSum = 100
  frameNumber = 0

  while 1:
    imageU16,sum = capture(flip_v = options.flip_v, device = options.device)
    if(sum != lastSum):
      lastSum = sum
      
      #or PNG, it can be the compression level ( CV_IMWRITE_PNG_COMPRESSION ) from 0 to 9. A higher value means a smaller size and longer compression time. Default value is 3.
      
      cv2.normalize(imageU16, imageU16, 0, 65535, cv2.NORM_MINMAX)
      np.right_shift(imageU16, 8, imageU16)
       
      cv2.imshow('MS8bit Norm frame', cv2.resize(np.uint8(imageU16), (80*4,60*4)))
      
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break