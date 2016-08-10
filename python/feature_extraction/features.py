import mahotas
import numpy as np
import cv2


def showCrop(inImg):
    resizeFactor = 8
    imgSize = tuple(resizeFactor * x for x in inImg.shape)
    inImg = cv2.resize(inImg, (imgSize[1], imgSize[0]))
    cv2.imshow('Crop', inImg)


def extractFeature(inImg, anno):
    # NOTE: its img[y: y + h, x: x + w]
    cropImg = inImg[int(anno[:].split(';')[4]):int(anno[:].split(';')[6]), int(anno[:].split(';')[3]):int(anno[:].split(';')[5])]
    # pad the image with extra white pixels to ensure the
    # edges of the objects are not up against the borders
    # of the image
    #featureImg = cv2.copyMakeBorder(cropImg, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    featureImg = cropImg
    # invert the image and threshold it
    #thresh = cv2.bitwise_not(image)
    #featureImg = cv2.GaussianBlur(cropImg, (3, 3), 0)
    ret2, th2 = cv2.threshold(featureImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # initialize the outline image, find the outermost
    # contours (the outline) of the pokemone, then draw
    # it
    outline = np.zeros(featureImg.shape, dtype="uint8")

    (outImg, contours, hierarchy) = cv2.findContours(th2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(outline, [contours], -1, 255, -1)
    showCrop(outline)
    # compute Zernike moments to characterize the shape
    # of the outline, then update the index
    # http://mahotas.readthedocs.org/en/latest/api.html#mahotas.features.zernike_moments
    moments = mahotas.features.zernike_moments(outline, 21)

    storeFeatures(moments, anno[:].split(';')[2])
    #print(clf.predict([moments]))