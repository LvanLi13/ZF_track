# Create ROIs automatically depend on 3 ROIs created by user
# ROIs have not points handle

import cv2
import os
import random

num_rows = 6
num_cols = 8
roi_radius = 30  # Radius for circular ROIs
selected_rois = []  # Store selected ROIs

# Function drawing circular ROIs
def draw_circular_rois(frame, rois):
    frame_copy = frame.copy()
    for roi in rois:
        cv2.circle(frame_copy, roi, roi_radius, (0, 255, 0), 2)
    return frame_copy

# Read video
video_path = 'E:\open\myenv\Resized_ZF_96p_240221.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Create 3 ROIs")
print("Press 'q' key to continue after creating the ROIs.")

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_rois.append((x, y))
        cv2.circle(frame_with_rois, (x, y), roi_radius, (0, 255, 0), 2)
        cv2.imshow('Select ROIs', frame_with_rois)

# Set up mouse callback
cv2.namedWindow('Select ROIs')
cv2.setMouseCallback('Select ROIs', mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_with_rois = draw_circular_rois(frame, selected_rois)
    cv2.imshow('Select ROIs', frame_with_rois)

    # Break loop when 3 ROIs are selected
    if cv2.waitKey(1) & 0xFF == ord('q') or len(selected_rois) == 3:
        break

cv2.destroyAllWindows()

# Create remaining ROIs in a matrix pattern
x_spacing = (width - 2 * roi_radius) // (num_cols - 1)
y_spacing = (height - 2 * roi_radius) // (num_rows - 1)
for i in range(num_rows):
    for j in range(num_cols):
        if i < 2 and j < 2:  # Skip corners
            continue
        x = roi_radius + j * x_spacing
        y = roi_radius + i * y_spacing
        selected_rois.append((x, y))

# Duplicate one ROI randomly in a new window
random_roi = random.choice(selected_rois)
random_roi_img = frame.copy()
cv2.circle(random_roi_img, random_roi, roi_radius, (0, 0, 255), 2)
cv2.imshow('Random ROI', random_roi_img)
cv2.waitKey(25)
cv2.destroyAllWindows()

# Create folder to save ROIs if not exists
output_folder = "Output_ROIs"
os.makedirs(output_folder, exist_ok=True)

# Save ROIs as file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_writers = []
for i, roi in enumerate(selected_rois):
    output_path = os.path.join(output_folder, f"ROI_00{i}.mp4")
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    video_writers.append(video_writer)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    for i, roi in enumerate(selected_rois):
        x, y = roi
        roi_frame = frame[max(0, y - roi_radius):min(height, y + roi_radius), 
                          max(0, x - roi_radius):min(width, x + roi_radius)]
        video_writers[i].write(roi_frame)

cap.release()
for video_writer in video_writers:
    video_writer.release()

print("ROIs saved successfully")
