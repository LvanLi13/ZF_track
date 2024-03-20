import cv2
import numpy as np

cap = cv2.VideoCapture('E:\open\myenv\ZF_96p_240221.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get the current frame size
    height, width, _ = frame.shape

    # Resize the frame
    scale_percent = 50
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)

    dim = (new_width, new_height)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(r'E:\open\myenv\Resized_ZF_96p_240221.mp4', fourcc, 30.0, dim)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        # Write the resized frame to the output video
        out.write(resized)

        # Display the resized frame to review
        cv2.imshow('Resized_ZF_96p_240221.mp4', resized)

        # Wait for a key press
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Release the video capture and writer and close all windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()