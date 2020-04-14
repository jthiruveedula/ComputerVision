# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 01:49:14 2020

@author: Jagadeesh Thiruveedula
""" 

import cv2
#eg: path ="haarcascade_frontalface_default.xml" for detecting face else you can give smile detecter also
faceCascade = cv2.CascadeClassifier(path)
video_capture  =cv2.VideoCapture(0)
#CAP_PROP_BUFFERSIZE for no lag video capture
video_capture.set(cv2.CAP_PROP_BUFFERSIZE,1)
count, buffer = 0,20
while(True):
    idx=0
    ret, frame = video_capture.read()
    if ret:
        count += 1
        if count == buffer:
            count=0
        elif count == 1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale( gray,scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            idx += 1
            cv2.putText(frame,"Face No: " +str(idx),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX,.7,(150,150,0),2)
            cv2.imshow('Face Detector',frame)
        if cv2.waitKey(1) == 13:
            break

cv2.destroyAllWindows()
video_capture.release()
