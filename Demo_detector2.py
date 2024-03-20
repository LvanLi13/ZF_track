# Source: https://pysource.com/2021/01/28/object-tracking-with-opencv-and-python/

import cv2
from tracker import *

tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("E:\open\myenv\Resized_ZF_96p_240221.mp4")

object_detector = cv2.createBackgroundSubtractorMOG2(history=400, varThreshold=190)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract ROI
    roi = frame[290: 350, 15:70]

    # Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 7:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            
            detections.append([x, y, w, h])

    # Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        #cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 1)
        #cv2.putText(frame, "ZF: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break