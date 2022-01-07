import cv2
import numpy as np
#from functions import track_maskHSL_live
def empty(a):
    pass

'''
AIM : capture live webcam, draw in air with different colours, replicate it on the video
'''
# cv2.namedWindow('Trackbars')
# cv2.createTrackbar('Brightness','Trackbars',120,179,empty)

cap = cv2.VideoCapture(0)
cap.set(10,120) #set brightness

#track_maskHSL_live(0,scale=0.5) #to find appropriate hsl values

myColors =[[5,107,0,19,255,255], #orange
           [133,56,0,159,156,255],  #purple
           #[57,76,0,100,255,255],   #green
           [47,44,0,83,143,255]]    #green2 #[h_min,s_min,v_min,h_max,s_max,v_max]
myColorVals = [(51,153,255),
               (255,0,255),
               #(0,255,0),
               (0,255,0)]
myPoints = [] #x,y,colorID

def getContours(img,imgResult,threshold=100):
    #shape_name = {3:'triangle',4:'rectangle',5:'pentagon',6:'hexagon',7:'septagon',8:'octagon'}
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #img,mode,method #cv2.RETR_EXTERNAL to get outer contours, cv2.CHAIN_APPROX_NONE gets all contours
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print('area : ',area,cnt.shape)
        if area>threshold: #to remove small noises
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)

            peri = cv2.arcLength(cnt,closed=True)
            #print('perimeter : ',peri)

            points = cv2.approxPolyDP(cnt,0.02*peri,True)   #curve,epsilon,closed
            objCorns = len(points)
            #print('corners : ',points.shape,objCorns)

            x,y,w,h = cv2.boundingRect(points)
            cv2.rectangle(imgResult,(x,y),(x+w,y+h),(0,255,0),3)

            # if objCorns<3:
            #     name = 'whattttt'
            # elif objCorns==4:
            #     if 0.95<w/h<1.05:
            #         name = 'square'
            #     else:
            #         name = 'rectangle'
            # elif 2<objCorns<9:
            #     name = shape_name[objCorns]
            # else:
            #     name = 'unknown'
            #
            # cv2.putText(imgResult,name,(x,y),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),5)

    #print(type(contours),hierarchy.shape)
    return x+w//2,y

def findColor(img,myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints=[]
    for i,myColor in enumerate(myColors):
        lower = np.array(myColor[0:3])
        upper = np.array(myColor[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)  # band pass filter
        imgMasked = cv2.bitwise_and(img, img, mask=mask)
        print(imgMasked.shape)
        x,y = getContours(mask,imgResult,threshold=1000)
        drawPoints(myPoints, myColorVals)
        cv2.circle(imgResult,(x,y),10,myColorVals[i],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append((x,y,i))
        #cv2.imshow(f'Colur{i}',imgResult)
    return newPoints

def drawPoints(myPoints,myColorVals):
    for pt in myPoints:
        cv2.circle(imgResult,(pt[0],pt[1]),10,myColorVals[pt[2]],cv2.FILLED)

while True:
    #cap.set(10, cv2.getTrackbarPos('Brightness','Trackbars'))
    success,img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors)
    if len(newPoints)!=0:
        myPoints += newPoints
    drawPoints(myPoints, myColorVals)
    cv2.imshow('Result',imgResult)
    # cv2.imshow('Result',imgColored)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

