import cv2
import numpy as np

img = cv2.imread('Resources/cat.png')
print(img.shape)  # height, weight, number of tonnels BGR

imgResize = cv2.resize(img, (256, 256))
print(imgResize.shape)

imgCropped = img[100:200, 0:200]

cv2.imshow('Image', img)
# cv2.imshow('Image resize', imgResize)
cv2.imshow('Cropped resize', imgCropped)

cv2.waitKey(0)
