import cv2
import numpy as np
from functions import stack_images

img = cv2.imread('resources/lena.png')
kernel = np.ones((5,5),np.uint8)

#change image look
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #note: opencv uses BGR by default
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)     # (7,7) is kernal size, must be odd number
imgCanny = cv2.Canny(imgGray,100,100) #edge detection
imgDialated = cv2.dilate(imgCanny,kernel,iterations=1) #join edges, more iterations more thick lines
imgEroded = cv2.erode(imgDialated,kernel,iterations = 1) #opposite of dialate

cv2.imshow('gray lena',imgGray)
cv2.imshow('blured lena',imgBlur)
cv2.imshow('edgy lena',imgCanny)
cv2.imshow('edgy dialated lena',imgDialated)
cv2.imshow('edgy dialated eroded lena',imgEroded)
cv2.waitKey(0)


#resize and crop
img = cv2.imread(r'resources\megumin_chibi.jpg')
img_shape = img.shape
print(img_shape)

imgResized = cv2.resize(img,(img_shape[0]//2,img_shape[1]//2))
imgCropped = imgResized[0:250,0:500] #note: order is height,width
print(imgResized.shape)

cv2.imshow('megubig',img)
cv2.imshow('megusmall',imgResized)
cv2.imshow('meguhat',imgCropped)
cv2.waitKey(0)

#warpPerspective
img = cv2.imread('resources/deathnote.jpg')

width,height = 224,300
pts1 = np.float32([[2,56],[111,11],[225,134],[112,193]])
pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])
tmatrix = cv2.getPerspectiveTransform(pts1,pts2)    #<class 'numpy.ndarray'>, transformation matrix
print(tmatrix.shape)

imgOutput = cv2.warpPerspective(img,tmatrix,(width,height))

cv2.imshow('image',img)
cv2.imshow('imageWarped',imgOutput)
cv2.waitKey(0)

#stack images
img = cv2.imread(r'resources\naruto_shadow.jpg')
print(img.shape)

imgHor = np.hstack((img,img))
imgVer = np.vstack((img,img))
imgStacked = stack_images([[img,img,img],[img,img,img]],0.5)

cv2.imshow('Hshadow_clones',imgHor)
cv2.imshow('Vshadow_clones',imgVer)
cv2.imshow('shadow_clones',imgStacked)
cv2.waitKey(0)

