import cv2
import numpy as np
import os
import matplotlib

drawing = False  # Kiểm tra trạng thái của việc vẽ ROI
ix, iy = -1, -1  # Tọa độ ban đầu của ROI
roi = None       # ROI được chọn

# Hàm mouse callback
def draw_rectangle_ROIs(event, x, y, flags, param):
    global ix, iy, drawing, roi

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            frame_draw = frame.copy()
            cv2.rectangle(frame_draw, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('name_of_experiment', frame_draw)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
        cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)
        cv2.imshow('name_of_experiment', frame)

# Hàm chia ROI thành ma trận các hình chữ nhật nhỏ
def divide_roi(roi, rows, cols):
    # Lấy kich thước ROI lớn
    roi_height, roi_width = roi.shape[:2]
    # Tính kích thước ROI nhỏ
    small_rect_height = roi_height // rows
    small_rect_width = roi_width // cols
    
    divided_ROIs = []

    for i in range(rows):
        for j in range(cols):
            x1 = j * small_rect_width
            y1 = i * small_rect_height
            x2 = (j + 1) * small_rect_width
            y2 = (i + 1) * small_rect_height
            divided_ROIs.append((x1, y1, x2, y2))

    return divided_ROIs

# Hàm vẽ ROI tròn quanh giếng
def draw_circular_ROIs(frame, rect):
    x1, y1, x2, y2 = rect
    # Tọa độ của trung điểm đường chéo
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    # Bán kính của đường tròn
    radius = min((x2 - x1), (y2 - y1)) // 2
    # Vẽ ROI là đường tròn nội tiếp
    cv2.circle(frame, (center_x, center_y), radius, (255, 0, 0), 2)

# Load video
video_path = 'E:\open\myenv\Resized_ZF_96p_240221.mp4'
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #Show video
    cv2.imshow('name_of_experiment', frame)

    #Draw ROI bao quanh
    cv2.setMouseCallback('name_of_experiment', draw_rectangle_ROIs)

    if roi is not None:
        # Setting ROI trên video gốc
        cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)
        
        # Show ROI trong cửa sổ mới
        roi_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
        cv2.imshow('ROI', roi_frame)

        # Copy ROI
        roi_copy = roi_frame.copy()

        # Chia ROI thành ma trận các hình chữ nhật nhỏ
        divided_ROIs = divide_roi(roi_copy, rows=6, cols=8)

        # Chia ROI thành ma trận các hình chữ nhật nhỏ
        for rect in divided_ROIs:
            x1, y1, x2, y2 = rect
            cv2.rectangle(roi_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Vẽ ROIs tròn quanh giếng
            draw_circular_ROIs(roi_copy, rect)

        # Hiển thị khung hình với ROI đã chia
        cv2.imshow('Divided_ROI', roi_copy)
    
    if cv2.waitKey(25) == 27:
        break

cap.release()
cv2.destroyAllWindows()