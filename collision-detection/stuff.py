import numpy as np
import cv2, socketio, random, time

# Create Socketio client
connection = socketio.Client()
print("Starting Socket.io")
connection.connect("https://cozmokart.site")
connection.send("lap 1")

# Start a timer
start_time = time.time()

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Background subtractor
backSub = cv2.createBackgroundSubtractorMOG2()

# Define minimum contour area for detection
MIN_CONTOUR_AREA = 500  

# Kernel for noise removal
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# Frame dimensions and ellipse parameters
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    cap.release()
    exit()

height, width, _ = frame.shape
center = (width // 2, height // 2 - 20)
axes_inner = (120, 60)  # (width, height) of the inner ellipse
axes_outer = (280, 140)  # (width, height) of the outer ellipse

def is_inside_ellipse(point, center, axes):
    """Check if a point is inside an ellipse using the standard equation."""
    x, y = point
    h, k = center
    a, b = axes
    return ((x - h) ** 2 / a ** 2 + (y - k) ** 2 / b ** 2) <= 1

count = 0
lapNumber = 1
checkpoints = [False, False, False]
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

    # Filter contours based on the ellipse region
    valid_contours = []
    for cnt in large_contours:
        for point in cnt:
            x, y = point[0]
            inside_outer = is_inside_ellipse((x, y), center, axes_outer)
            outside_inner = not is_inside_ellipse((x, y), center, axes_inner)
            
            inside_inner = is_inside_ellipse((x,y), center, axes_inner)
            outside_outer = not is_inside_ellipse((x,y), center, axes_outer) and y < 420 and y > 50
            
            # Check if checkpoints are hit, increment lap count if all are hit and at goal
            if x > 310 and x < 330 and y < height // 2 - 20 and all(checkpoints):
                lapNumber += 1
                connection.send("lap " + str(lapNumber))
                checkpoints = [False, False, False]
                print("Lap Complete!")
            elif x > 480 and y > 200 and y < 280:
                if (not checkpoints[0]):
                    print("Checkpoint 1 active!")
                checkpoints[0] = True
            elif x < 160 and y > 200 and y < 280:
                if (not checkpoints[2]):
                    print("Checkpoint 3 active!")
                checkpoints[2] = True
            elif x > 280 and x < 360 and y > 280:
                if (not checkpoints[1]):
                    print("Checkpoint 2 active!")
                checkpoints[1] = True
            

            if inside_inner or outside_outer:
                valid_contours.append(cnt)
                count += 1
                print("COLLISION" + int(random.random() * 10))
                connection.send("stop_up") # Stop robot
                
                break  # If any point of the contour is valid, keep the whole contour
                

    # Draw contours
    frame_ct = frame.copy()
    cv2.drawContours(frame_ct, valid_contours, -1, (0, 255, 0), 2)

    # Draw ellipses
    cv2.ellipse(frame_ct, center, axes_inner, 0, 0, 360, (255, 0, 0), 3)
    cv2.ellipse(frame_ct, center, axes_outer, 0, 0, 360, (255, 0, 0), 3)
    cv2.line(frame_ct, (center[0], center[1] - axes_inner[1]), (center[0], center[1] - axes_outer[1]), (0,0,255), 2)
    
    # Draw Lap Count
    #font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (50, 50)

    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2
    cv2.putText(
        frame_ct, 
        f"Lap:{str(lapNumber)} Time: {str((int(1000*(time.time() - start_time))/1000))}", org, font, fontScale, color, thickness, cv2.LINE_AA)

    # Display frame
    cv2.imshow('Contours with Ellipse', frame_ct)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
