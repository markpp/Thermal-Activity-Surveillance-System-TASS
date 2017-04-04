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
                    action="store_true", dest="flip_v", default=True,
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

  # File structure to be created based on timestamp
  dirPath = "/home/pi/Desktop/output/" + timeNowString + "/"
  vidPath = "/home/pi/Desktop/output/"
  if not os.path.exists(dirPath):
    os.mkdir( dirPath );
  else:
    dirPath = "/home/pi/Desktop/outputAlt/" + timeNowString + "/"
    vidPath = "/home/pi/Desktop/outputAlt/"
    os.makedirs( dirPath )
  print "Path is: " + dirPath
  print "Capturing..."

  # Codec selection 
  #fourcc = cv2.cv.CV_FOURCC('Z','L','I','B')
  #fourcc = cv2.cv.CV_FOURCC('L','J','P','G')
  #fourcc = cv2.cv.CV_FOURCC('X','2','6','4')
  #fourcc = cv2.cv.CV_FOURCC('Y','U','Y','2')
  fourcc = cv2.cv.CV_FOURCC('H','F','Y','U')
  #fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
  #videoOutMS8 = cv2.VideoWriter('/home/pi/Desktop/output/' + timeNowString + 'outputMS8.avi',fourcc, 9, (80,60), False)
  #videoOutLS8 = cv2.VideoWriter('/home/pi/Desktop/output/' + timeNowString + 'outputLS8.avi',fourcc, 9, (80,60), False)
  videoOutMS8Norm = cv2.VideoWriter(vidPath + timeNowString + 'outputMS8Norm.avi',fourcc, 9, (80,60), 0)
  #videoOutColor = cv2.VideoWriter('/home/pi/Desktop/output/' + timeNowString + 'outputColor.avi',fourcc, 9, (80,60), True)
  sum = -1
  lastSum = 100
  frameNumber = 0
  try:
    while 1:
      imageU16,sum = capture(flip_v = options.flip_v, device = options.device)
      
      '''    
      LS8 = np.uint8(imageU16) # store 8 least significant bits
      MS8 = np.uint8(np.right_shift(imageU16,8 )) # store 8(4) most significant bits
      imgCombined = cv2.merge(( LS8 , MS8 , LS8 )) # store all bits in color frame
      cv2.imshow('Color packed frame', cv2.resize(imgCombined, (80*4,60*4)))
      #cv2.imshow('imageU16', cv2.resize(imageU16, (80*4,60*4)))
      '''
      
      if(sum != lastSum):
        lastSum = sum
        filePath = dirPath + "frame_" + str(frameNumber).zfill(6) + ".png"
        #or PNG, it can be the compression level ( CV_IMWRITE_PNG_COMPRESSION ) from 0 to 9. A higher value means a smaller size and longer compression time. Default value is 3.
        cv2.imwrite(filePath, imageU16) # write full 16bit(12) image to disk, minimum compression 0
        frameNumber = frameNumber + 1
        '''
        cv2.imwrite('MS8bit.png', MS8)
        cv2.imwrite('LS8bit.png', LS8)
        #print sum
        videoOutMS8.write(MS8)
        videoOutLS8.write(LS8)
        videoOutColor.write(imgCombined)
        '''
        cv2.normalize(imageU16, imageU16, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(imageU16, 8, imageU16)
        videoOutMS8Norm.write(np.uint8(imageU16))

        #cv2.imshow('MS8bit Norm frame', cv2.resize(np.uint8(imageU16), (80*4,60*4)))
      
      #cv2.waitKey()
      #if cv2.waitKey(10) & 0xFF == ord('q'):
        #break

  except KeyboardInterrupt:
    
    videoOutMS8Norm.release()
    #videoOutMS8.release()
    #videoOutLS8.release()
    #videoOutColor.release()
    #cv2.destroyAllWindows()
    #os.system('reboot -f')
