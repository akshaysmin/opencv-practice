import cv2
import numpy as np
from functions import stack_images

####
imgWidth,imgHeight = 640,480
####
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,120)

def preProcess(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv2.erode(imgDial,kernel,iterations=1)
    return imgThres

def getBiggestContour(img,imgResult,threshold=100):
    #shape_name = {3:'triangle',4:'rectangle',5:'pentagon',6:'hexagon',7:'septagon',8:'octagon'}
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #img,mode,method #cv2.RETR_EXTERNAL to get outer contours, cv2.CHAIN_APPROX_NONE gets all contours
    maxArea = 0
    biggest = np.array([[[200,200]],[[400,200]],[[200,400]],[[400,400]]]) #default value
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print('area : ',area,cnt.shape)
        if area>threshold: #to remove small noises
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,closed=True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)   #curve,epsilon,closed
            objCorns = len(approx)
            #print('corners : ',approx.shape,objCorns)
            if area>maxArea and objCorns==4:
                biggest = approx
                maxArea = area
            x,y,w,h = cv2.boundingRect(approx)
            #cv2.rectangle(imgResult,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.drawContours(imgResult, biggest, -1, (255, 0, 0), 20)
    return biggest

def orderPoints(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)

    add = myPoints.sum(axis=1)
    diff = np.diff(myPoints,axis=1)
    print('add',add)
    print('diff',diff)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]

    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    print(myPointsNew)
    return myPointsNew

def getWarp(img,biggest):
    pts1 = np.float32(biggest)    #np.float32([[2, 56], [111, 11], [225, 134], [112, 193]])
    pts2 = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])

    tmatrix = cv2.getPerspectiveTransform(pts1, pts2)  # <class 'numpy.ndarray'>, transformation matrix
    imgOutput = cv2.warpPerspective(img, tmatrix, (imgWidth, imgHeight))

    return imgOutput

while True:
    success,img = cap.read()
    img = cv2.resize(img, (imgWidth, imgHeight))
    imgResult = img.copy()
    imgThres = preProcess(img)
    biggest = getBiggestContour(imgThres, imgResult, threshold=100)
    print(biggest)
    biggest = orderPoints(biggest)

    imgWarped = getWarp(img,biggest)
    imgCropped = imgWarped[20:-20,20:-20]
    imgCropped = cv2.resize(imgCropped,(imgWidth,imgHeight))

    imgStacked = stack_images([[img,imgThres],[imgResult,imgCropped]],scale=0.5)
    # cv2.imshow('Result',imgResult)
    # cv2.imshow('Warped Result',imgWarped)
    cv2.imshow('Cropped',imgCropped)
    cv2.imshow('document scanning',imgStacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
