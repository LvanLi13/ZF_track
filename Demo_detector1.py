#import nessecary library
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#load video and show frame
cap = cv2.VideoCapture('E:\open\myenv\Resized_ZF_96p_240221.mp4')

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    #Find difference between 1st frame and 2nd frame
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 200:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame1, "ZF: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        #cv2.drawContours(frame1, contours, -1, (0,255,0), 2)

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()

