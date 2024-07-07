import numpy as np
import cv2
import pytesseract
import time


def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    bounding_boxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, bounding_boxes) = zip(*sorted(zip(cnts, bounding_boxes),
                                         key=lambda b: b[1][i], reverse=reverse))
    return cnts, bounding_boxes

def get_transformed_perspective(frame, pts):
    # crop image
    height, width, _ = frame.shape
    frame = frame[0:height - 200, 250:width - 250]

    # Define the destination points for perspective transform (corners of a square)
    size = max(width, height)
    pts_dst = np.array([
        [0, 0],  # Top-left
        [size - 1, 0],  # Top-right
        [0, size - 1],  # Bottom-left
        [size - 1, size - 1]  # Bottom-right
    ], dtype='float32')

    # Get the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts, pts_dst)

    # Apply the perspective transformation
    square_roi = cv2.warpPerspective(frame, matrix, (size, size))
    return square_roi
def view_sample(pts):
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()

        square_roi = get_transformed_perspective(frame, pts)

        # Display the original image and the transformed square ROI
        cv2.imshow('Detected Red Rectangles', frame)
        cv2.imshow('Square ROI', square_roi)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def get_letters(pts):
    time.sleep(5)
    # Capture a frame from the webcam
    vid = cv2.VideoCapture(0)
    ret, frame = vid.read()
    vid.release()  # Release the video capture object

    image = get_transformed_perspective(frame, pts)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to get a binary image
    _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Invert the image if necessary (if the letters are black on white background)
    mask = cv2.bitwise_not(mask)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Find contours of the letters
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours from top to bottom, left to right

    contours, _ = sort_contours(contours, method="top-to-bottom")

    # Initialize an empty list to store recognized letters
    recognized_letters = []
    grid_order = []

    # Loop over the contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 10 and h > 10:  # filter out small noise
            shrink = 35
            # Extract the letter
            letter_image = mask[y + shrink:y + h - shrink, x + shrink:x + w - shrink]

            # Add padding to the letter image
            padding = 0
            letter_image = cv2.copyMakeBorder(letter_image, padding, padding, padding, padding, cv2.BORDER_CONSTANT,
                                              value=[255, 255, 255])

            # Resize the letter image to a fixed size (e.g., 28x28 pixels) to standardize input for OCR
            letter_image = cv2.resize(letter_image, (28, 28))

            # Use Tesseract to recognize the letter
            letter = pytesseract.image_to_string(letter_image,
                                                 config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0')

            letter = letter[0].upper()

            recognized_letters.append(letter.strip().lower())
            grid_order.append([(x + 50) // 400, (y + 50) // 400])

            # Draw the bounding box and recognized letter on the original image (for visualization purposes)
            cv2.rectangle(image, (x + shrink, y + shrink), (x + w - shrink, y + h - shrink), (0, 255, 0), 2)
            cv2.putText(image, letter.strip(), (x + shrink + 10, y + shrink + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Recognized Letters', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Print the recognized letters
    print("Recognized Letters:", recognized_letters)
    grid = [[0 for _ in range(4)] for _ in range(4)]

    for coord in grid_order:
        grid[coord[1]][coord[0]] = recognized_letters.pop(0)
    print(grid)
    return grid