import numpy as np
import cv2
import os
import argparse
from matplotlib import pyplot as plt


def background_threshold(frame):
    histogram_threshold(frame)
    return otsu_threshold(frame)


def otsu_threshold(frame):
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(frame, (3, 3), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def histogram_threshold(frame):
    hist_size = 256
    hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(hist)
    print max_loc
    #return th3


def investigate_threshold(frame):
    """Try different threshold types a visualize the results.

    otsu:

    Args:
        frame (np.array): Input frame.

    """

    ret1, th1 = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

    ret2, th2 = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(frame, (3, 3), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #print th3

    # plot all the images and their histograms
    images = [frame, 0, th1,
              frame, 0, th2,
              blur, 0, th3]
    titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
              'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
              'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

    for i in xrange(3):
        plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
        plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
        plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
        plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])
    plt.show()


