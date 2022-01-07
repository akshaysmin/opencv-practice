import cv2
import numpy as np

def stack_images(imgArray,scale=1):
    '''
    imgArray must be 2d ->rows stacked horizontally, columns vertically
    all images must be of same size
    all images must be of type <class 'numpy.ndarray'>
    scale is to resize
    '''
    hstacked = []
    for imgRow in imgArray:
        for i,image in enumerate(imgRow):
            if len(image.shape)!=3:    #I,m trying to catch images that are grayscale
                imgRow[i] = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        hstacked.append(np.hstack(imgRow))
    stackedimg = np.vstack(hstacked)
    scaled_shape = (int(stackedimg.shape[0]*scale),int(stackedimg.shape[1]*scale))

    return cv2.resize(stackedimg,scaled_shape)

def empty(a):
    pass

def track_maskHSL(img,scale=1):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #create window with trackbars
    cv2.namedWindow('TrackBars')
    cv2.resizeWindow('TrackBars',640,240)
    cv2.createTrackbar('Hue Min','TrackBars',110,179,empty)
    cv2.createTrackbar('Hue Max','TrackBars',178,179,empty)
    cv2.createTrackbar('Sat Min','TrackBars',218,255,empty)
    cv2.createTrackbar('Sat Max','TrackBars',255,255,empty)
    cv2.createTrackbar('Val Min','TrackBars',36,255,empty)
    cv2.createTrackbar('Val Max','TrackBars',255,255,empty)

    #play with trackbars and mask image in realtime
    while True:
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

        imgStacked = stack_images([[img,imgHSV],[cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR),imgMasked]],scale=scale)
        cv2.imshow('image masking steps',imgStacked)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def track_maskHSL_live(source=0,scale=1):
    cap = cv2.VideoCapture(source)

    #create window with trackbars
    cv2.namedWindow('TrackBars')
    cv2.resizeWindow('TrackBars',640,240)
    cv2.createTrackbar('Hue Min','TrackBars',110,179,empty)
    cv2.createTrackbar('Hue Max','TrackBars',178,179,empty)
    cv2.createTrackbar('Sat Min','TrackBars',218,255,empty)
    cv2.createTrackbar('Sat Max','TrackBars',255,255,empty)
    cv2.createTrackbar('Val Min','TrackBars',36,255,empty)
    cv2.createTrackbar('Val Max','TrackBars',255,255,empty)

    #play with trackbars and mask image in realtime
    while True:
        success,img = cap.read()
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

        imgStacked = stack_images([[img,imgHSV],[cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR),imgMasked]],scale=scale)
        cv2.imshow('image masking steps',imgStacked)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


