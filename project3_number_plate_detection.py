import cv2
import numpy as np
import os #just to make output folder

cv2.imwrite('outputs/test.jpg',cv2.imread('resources/ginsan_chibi.jpg'))

####
imgWidth,imgHeight = 640,480
minArea = 0
outpath = 'outputs/number_plates' # IMPORTANT : this folder needs to already exist
####

if not os.path.exists(outpath):
    os.makedirs(outpath)

cap = cv2.VideoCapture('resources/traffic_picpoc.mp4')
cap.set(3,640)
cap.set(4,480)
cap.set(10,120)

numplateCascade = cv2.CascadeClassifier('resources/haarcascade_russian_plate_number.xml')

j=0
while True:
    j+=1
    success,img = cap.read()
    img = cv2.imread('resources/numplate.jpg')
    img = cv2.resize(img,(imgWidth,imgHeight))
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    plates = numplateCascade.detectMultiScale(imgGray, 1.1, 4)  # img,scale,nearest_neighbours

    for x, y, w, h in plates:
        area = w*h
        if area>minArea:
            imgNumPlate = img[y:y+h,x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h),(0, 300, 300), 3)
            cv2.putText(img,'number plate',(x,y),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)

    cv2.imshow('Result',img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'{outpath}/{j}_allNumPlates.jpg',img)
        i=0
        for x, y, w, h in plates:
            area = w * h
            if area > minArea:
                i+=1
                imgNumPlate = img[y:y + h, x:x + w]
                cv2.imwrite(f'{outpath}/{j}_{i}.jpg',imgNumPlate)
        cv2.putText(img,'image saved',(0,200),cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),5)
        cv2.imshow('Result', img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
