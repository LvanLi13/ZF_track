


import cv2
import os
import random
import numpy as np

selected_rois = []  # Store manually selected ROIs
output_folder = "Output_ROIs"  # Save ROI
num_rows = 12
num_cols = 8
roi_radius = 30

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read video
vid_path = 'E:\open\myenv\Resized_ZF_96p_240221.mp4'
cap = cv2.VideoCapture(vid_path)

# Function drawing circular ROIs
def draw_circular_rois(frame):
    frame_copy = frame.copy()
    for roi in selected_rois:
        cv2.circle(frame_copy, roi, roi_radius, (0, 255, 0), 2)
    return frame_copy

# Function selecting ROIs
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_rois.append((x, y))
        if len(selected_rois) == 3:
            cv2.setMouseCallback('Select ROIs', lambda *args: None)

print("Create 3 ROIs") # To click. Need to optimize
print("Press any key to continue")

cv2.namedWindow('Select ROIs')
cv2.setMouseCallback('Select ROIs', mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Draw circular ROIs
    frame_with_rois = draw_circular_rois(frame)
    cv2.imshow('Select ROIs', frame_with_rois)

    if len(selected_rois) == 3:
        cv2.waitKey(0)
        break

# Check if any ROIs are selected
if len(selected_rois) != 3:
    print("Error: Please select 3 circular ROIs")
    exit()

# Calculate bounding rectangle
# Need to optimize
x_values = [x for x, y in selected_rois]
y_values = [y for x, y in selected_rois]
x_min, x_max = min(x_values) - roi_radius, max(x_values) + roi_radius
y_min, y_max = min(y_values) - roi_radius, max(y_values) + roi_radius

# Create remaining ROIs
rois = []
for i in range(num_rows):
    for j in range(num_cols):
        x = x_min + (j * (x_max - x_min)) // num_cols
        y = y_min + (i * (y_max - y_min)) // num_rows
        rois.append((x, y))

"""
# Randomly select one ROI
random_roi = random.choice(rois)
random_roi_x, random_roi_y = random_roi
random_roi_img = frame.copy()
cv2.circle(random_roi_img, (random_roi_x, random_roi_y), roi_radius, (0, 0, 255), 2)

# Display random ROI in a new window to check   # Need to optimize
cv2.imshow('Random ROI', random_roi_img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""

# Save ROIs as file     # Need to optimize for saving ROIs as videos
for i, (x, y) in enumerate(rois):
    roi_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    cv2.circle(roi_img, (x, y), roi_radius, (255, 255, 255), -1)
    cv2.imwrite(os.path.join(output_folder, f"roi_{i}.jpg"), roi_img)

cap.release()

print("ROIs saved successfully.")
