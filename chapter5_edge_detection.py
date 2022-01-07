import cv2
import numpy as np
from functions import stack_images

'''
Summary:
#BGR -> GREY -> blur -> canny -> findContours -> drawContours -> draw boundingRectanle
'''

img = cv2.imread('resources/avatar_elements.jpg')
img = cv2.imread('resources/shapes.webp')
scale = 0.25

#img = cv2.imread('resources/shapes.jpg')
imgBlur = cv2.GaussianBlur(img,(5,5),1)
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgGrayB = cv2.GaussianBlur(imgGray,(5,5),1)
#imgBlank = np.zeros_like(img)

imgCanny = cv2.Canny(img,50,50)
imgCannyB = cv2.Canny(imgBlur,50,50)
imgCannyG = cv2.Canny(imgGray,50,50)
imgCannyGB = cv2.Canny(imgGrayB,50,50) #note: grey blurred images detect edges better

print(img.shape,imgBlur.shape,imgCanny.shape,imgCannyB.shape)
print(imgGray.shape,imgGrayB.shape,imgCannyG.shape,imgCannyGB.shape)

imgStack0 = stack_images([[img,imgBlur],[imgCanny,imgCannyB]],scale)
imgStack1 = stack_images([[imgGray,imgGrayB],[imgCannyG,imgCannyGB]],scale)
print(imgStack0.shape)
print(imgStack1.shape)
cv2.imshow('BGR Edge Detection',imgStack0)
cv2.imshow('GRAY Edge Detection',imgStack1)
# cv2.waitKey(0)

def getContours(img,imgContour):
    shape_name = {3:'triangle',4:'rectangle',5:'pentagon',6:'hexagon',7:'septagon',8:'octagon'}
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #img,mode,method #cv2.RETR_EXTERNAL to get outer contours, cv2.CHAIN_APPROX_NONE gets all contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print('area : ',area,cnt.shape)
        if area>100: #to remove small noises
            cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)

            peri = cv2.arcLength(cnt,closed=True)
            print('perimeter : ',peri)

            points = cv2.approxPolyDP(cnt,0.02*peri,True)   #curve,epsilon,closed
            objCorns = len(points)
            print('corners : ',points.shape,objCorns)

            x,y,w,h = cv2.boundingRect(points)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),3)

            if objCorns<3:
                name = 'whattttt'
            elif objCorns==4:
                if 0.95<w/h<1.05:
                    name = 'square'
                else:
                    name = 'rectangle'
            elif 2<objCorns<9:
                name = shape_name[objCorns]
            else:
                name = 'unknown'

            cv2.putText(imgContour,name,(x,y),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),5)

    print(type(contours),hierarchy.shape)

imgContour = img.copy()
getContours(imgCannyGB,imgContour)
imgStack2 = stack_images([[img,imgCannyGB],[imgCannyG,imgContour]],scale)
cv2.imshow('Contour Detection',imgStack2)
cv2.waitKey(0)
print(imgContour.shape)
