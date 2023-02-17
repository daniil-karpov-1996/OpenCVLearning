import cv2
import numpy as np

img = cv2.imread('Resources/cat.png')

imgHor = np.hstack((img, img))
imgVer = np.vstack((img, img))

cv2.imshow('Image double hor', imgHor)
cv2.imshow('Image double ver', imgVer)

cv2.waitKey(0)
