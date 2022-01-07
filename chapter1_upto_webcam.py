import cv2


#pic
img = cv2.imread("resources\hayasaka_chibi.png") # <class 'numpy.ndarray'>
cv2.imshow("Hayasaka",img)
cv2.waitKey(0)

#video
cap = cv2.VideoCapture(r"resources\sparkle_your_name.mp4")
while True:
    success, img = cap.read()
    cv2.imshow('Video',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#webcam
cap = cv2.VideoCapture(0) # use 0,1,2, etc. for different cams attached to pc
cap.set(3,640)  #set width
cap.set(4,480)  #set height
cap.set(10,1000) #set brightness
while True:
    success,img = cap.read()
    cv2.imshow('Video',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
