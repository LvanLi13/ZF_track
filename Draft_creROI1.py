#Create ROIs with points handle that are interactive adjustment, mean resizable and movable  

import cv2
import os
import random
from math import cos, sin, radians
import numpy as np

roi_radius = 30  # Radius for circular ROIs
selected_roi_index = None  # Index of the selected ROI
selected_handle_index = None  # Index of the selected handle within the ROI
selected_handle_offset = (0, 0)  # Offset of the mouse click from the handle position

# Function for drawing circular ROIs with handles
def draw_circular_rois_with_handles(frame, rois):
    frame_copy = frame.copy()
    for i, roi in enumerate(rois):
        for j, point in enumerate(roi):
            if i == selected_roi_index and j == selected_handle_index:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            cv2.circle(frame_copy, point, 5, color, -1)
            if j < len(roi) - 1:
                cv2.line(frame_copy, point, roi[j + 1], color, 2)
            if j == len(roi) - 1:
                cv2.line(frame_copy, point, roi[0], color, 2)
    return frame_copy

# Function for creating circular ROI with handles
def create_roi_with_handles(center):
    roi = []
    for angle in range(0, 360, 45):
        x = int(center[0] + roi_radius * cos(radians(angle)))
        y = int(center[1] + roi_radius * sin(radians(angle)))
        roi.append((x, y))
    return roi

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global selected_roi_index, selected_handle_index, selected_handle_offset, rois
    if (event == cv2.EVENT_LBUTTONDOWN):
        # Check if a handle was clicked
        for i, roi in enumerate(rois):
            for j, point in enumerate(roi):
                distance = ((x - point[0]) ** 2 + (y - point[1]) ** 2) ** 0.5
                if distance <= 5:  # Check if clicked point is within 5 pixels of any ROI handle
                    selected_roi_index = i
                    selected_handle_index = j
                    selected_handle_offset = (point[0] - x, point[1] - y)
                    return
        # If no handle clicked, create a new ROI
        rois.append(create_roi_with_handles((x, y)))
        selected_roi_index = len(rois) - 1
    elif event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON:
        # If left mouse button is pressed and moving, adjust the selected handle position
        # Need to optimize
        if (selected_roi_index is not None) and (selected_handle_index is not None):
            x = max(min(x, width - 1), 0)  # Limit x coordinate within the frame
            y = max(min(y, height - 1), 0)  # Limit y coordinate within the frame
            rois[selected_roi_index][selected_handle_index] = (x + selected_handle_offset[0], y + selected_handle_offset[1])

# Read video
video_path = 'E:\open\myenv\Resized_ZF_96p_240221.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Create ROIs")
print("Press 'c' key to continue")

# Mouse callback
cv2.namedWindow('Select ROIs')
cv2.setMouseCallback('Select ROIs', mouse_callback)

# List for ROIs stored
rois = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_with_rois = draw_circular_rois_with_handles(frame, rois)
    cv2.imshow('Select ROIs', frame_with_rois)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cv2.destroyAllWindows()

# Create folder to save ROIs if not exists
output_folder = "Output_ROIs"
os.makedirs(output_folder, exist_ok=True)

# Save ROIs as videos
# Bug: Video ROIs is not displayed
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_writers = []
for i, roi in enumerate(rois):
    output_path = os.path.join(output_folder, f"ROI_00{i}.mp4")
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    video_writers.append(video_writer)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
# Process video and save ROIs
for i, roi in enumerate(rois):
    # Check if ROI is empty
    if not roi:
        print(f"ROI_00{i} is empty")
        continue

    # Write the ROI frame to the corresponding video file
video_writers[i].write(roi)

    # Display the ROI frame
cv2.imshow(f"ROI_00{i}", roi)
cv2.waitKey(25)

cap.release()
for video_writer in video_writers:
    video_writer.release()

print("ROIs saved successfully")


