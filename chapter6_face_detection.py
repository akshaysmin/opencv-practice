import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#viola and john's method

faceCascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('resources/haarcascade_eye.xml')

def face_detect(img):
	img = img.copy()
	imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	
	faces = faceCascade.detectMultiScale(imgGray,1.1,4) #img,scale,nearest_neighbours
	eyes = eyeCascade.detectMultiScale(imgGray,1.1,4)
	
	for x,y,w,h in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(0,300,300),3)
	
	for x,y,w,h in eyes:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(300,300,0),3)

	return img
	
img = cv2.imread('resources/lena.png')
#img = cv2.imread(r'resources\naruto_shadow.jpg') # note: anime faces are not detected
cv2.imshow('Face Detection',face_detect(img))
cv2.waitKey(0)

while True:
	success, img = cap.read()
	#cv2.imshow('Cam Face Detection',img)
	cv2.imshow('Cam Face Detection',face_detect(img))
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break