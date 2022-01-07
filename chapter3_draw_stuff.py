import cv2
import numpy as np


#draw shapes
img = np.zeros((512,512,3),np.uint8)
img[:] = 100,100,100 # set BGR of whole image

cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),5) #img,pt1,pt2,color,thickness
cv2.rectangle(img,(100,100),(200,200),(0,0,255),3)  #rectangle
cv2.rectangle(img,(250,250),(400,400),(0,0,255),cv2.FILLED) #filled rectangle
cv2.circle(img,(350,120),50,(100,200,0),10) #img,centre,radius,color,thickness

cv2.putText(img,'opencv', (250,230),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,150,0),2) #img,text,location,font,scale,color,thickness

cv2.imshow('image',img)
cv2.waitKey(0)



