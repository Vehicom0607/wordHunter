import cv2
import numpy as np

# Capture a frame from the webcam
vid = cv2.VideoCapture(0)
ret, frame = vid.read()
vid.release()  # Release the video capture object

if not ret:
    print("Failed to capture image")
    exit()

height, width, _ = frame.shape
frame = frame[0:height - 200, 250:width-250]

# Convert the image to HSV format
image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define the target color range in HSV
lower_red = np.array([0, 100, 100])  # Adjust as needed
upper_red = np.array([10, 255, 255])  # Adjust as needed
lower_red2 = np.array([160, 100, 100])  # Adjust as needed for red wrapping around in HSV
upper_red2 = np.array([180, 255, 255])  # Adjust as needed

# Create a mask for red color
mask1 = cv2.inRange(image_hsv, lower_red, upper_red)
mask2 = cv2.inRange(image_hsv, lower_red2, upper_red2)
mask = mask1 | mask2

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# List to store bounding boxes of the detected rectangles
bounding_boxes = []

# Draw rectangles around the detected contours
for contour in contours:
    area = cv2.contourArea(contour)
    if 100 < area < 5000:  # Adjust the area thresholds as needed
        x, y, w, h = cv2.boundingRect(contour)
        bounding_boxes.append((x, y, w, h))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Ensure we have exactly four rectangles
if len(bounding_boxes) != 4:
    print("Did not detect exactly four rectangles")
    exit()

# Sort the bounding boxes to get the four corners
bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))  # Sort by y then x
if bounding_boxes[0][0] > bounding_boxes[1][0]:
    bounding_boxes[0], bounding_boxes[1] = bounding_boxes[1], bounding_boxes[0]
if bounding_boxes[2][0] > bounding_boxes[3][0]:
    bounding_boxes[2], bounding_boxes[3] = bounding_boxes[3], bounding_boxes[2]

# Get the corner points from the bounding boxes
pts_src = np.array([
    [bounding_boxes[0][0], bounding_boxes[0][1]],  # Top-left
    [bounding_boxes[1][0] + bounding_boxes[1][2], bounding_boxes[1][1]],  # Top-right
    [bounding_boxes[2][0], bounding_boxes[2][1] + bounding_boxes[2][3]],  # Bottom-left
    [bounding_boxes[3][0] + bounding_boxes[3][2], bounding_boxes[3][1] + bounding_boxes[3][3]]  # Bottom-right
], dtype='float32')

# Define the destination points for perspective transform (corners of a square)
size = max(width, height)
pts_dst = np.array([
    [0, 0],  # Top-left
    [size - 1, 0],  # Top-right
    [0, size - 1],  # Bottom-left
    [size - 1, size - 1]  # Bottom-right
], dtype='float32')

# Get the perspective transform matrix
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

# Apply the perspective transformation
square_roi = cv2.warpPerspective(frame, matrix, (size, size))

# Display the original image and the transformed square ROI
cv2.imshow('Detected Red Rectangles', frame)
cv2.imshow('Square ROI', square_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(pts_src)


# Part 2
vid = cv2.VideoCapture(0)
while True:
    ret, frame = vid.read()

    # crop image
    height, width, _ = frame.shape
    frame = frame[0:height - 200, 250:width - 250]

    cv2.imshow("Video", frame)

    # Define the destination points for perspective transform (corners of a square)
    size = max(width, height)
    pts_dst = np.array([
        [0, 0],  # Top-left
        [size - 1, 0],  # Top-right
        [0, size - 1],  # Bottom-left
        [size - 1, size - 1]  # Bottom-right
    ], dtype='float32')

    # Get the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Apply the perspective transformation
    square_roi = cv2.warpPerspective(frame, matrix, (size, size))

    # Display the original image and the transformed square ROI
    cv2.imshow('Detected Red Rectangles', frame)
    cv2.imshow('Square ROI', square_roi)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()