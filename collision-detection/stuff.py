import cv2
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture(2)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Background subtractor
backSub = cv2.createBackgroundSubtractorMOG2()

# Define minimum contour area for detection
MIN_CONTOUR_AREA = 500  

# Kernel for noise removal
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Apply background subtraction
    fg_mask = backSub.apply(frame)

    # Apply thresholding to refine mask
    _, mask_thresh = cv2.threshold(fg_mask, 180, 255, cv2.THRESH_BINARY)

    # Noise removal with morphological opening
    mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter large moving objects
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > MIN_CONTOUR_AREA]

    # Draw contours
    frame_ct = frame.copy()
    cv2.drawContours(frame_ct, large_contours, -1, (0, 255, 0), 2)

    # Display frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Processed Mask', mask_eroded)
    cv2.imshow('Contours', frame_ct)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
