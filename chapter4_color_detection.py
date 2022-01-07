import cv2
import numpy as np
from functions import stack_images


path = r'resources/capshield_small.png'
#cv2.imwrite('capshield_small.png',cv2.resize(cv2.imread(path),(500,500)))

#create window with trackbars
def empty(a):
    pass
cv2.namedWindow('TrackBars')
cv2.resizeWindow('TrackBars',640,240)
cv2.createTrackbar('Hue Min','TrackBars',110,179,empty) #trackbarName,WindowName,default,max,function to which the value is passed
cv2.createTrackbar('Hue Max','TrackBars',178,179,empty)
cv2.createTrackbar('Sat Min','TrackBars',218,255,empty)
cv2.createTrackbar('Sat Max','TrackBars',255,255,empty)
cv2.createTrackbar('Val Min','TrackBars',36,255,empty)
cv2.createTrackbar('Val Max','TrackBars',255,255,empty)

#play with trackbars and mask image in realtime
while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('Hue Min','TrackBars')
    h_max = cv2.getTrackbarPos('Hue Max','TrackBars')
    s_min = cv2.getTrackbarPos('Sat Min','TrackBars')
    s_max = cv2.getTrackbarPos('Sat Max','TrackBars')
    v_min = cv2.getTrackbarPos('Val Min','TrackBars')
    v_max = cv2.getTrackbarPos('Val Max','TrackBars')
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper) #band pass filter
    imgMasked = cv2.bitwise_and(img,img,mask=mask)

    imgStacked = stack_images([[img,imgHSV],[cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR),imgMasked]],scale=0.5)
    cv2.imshow('image masking steps',imgStacked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


