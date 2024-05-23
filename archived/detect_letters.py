import cv2
import numpy as np
import pytesseract

# Load the image
image = cv2.imread('images/small_grid.png')

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
    return (cnts, bounding_boxes)

contours, _ = sort_contours(contours, method="top-to-bottom")

# Initialize an empty list to store recognized letters
recognized_letters = []
grid_order = []

# Loop over the contours
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 10 and h > 10:  # filter out small noise
        shrink = 45
        # Extract the letter
        letter_image = mask[y + shrink:y + h - shrink, x + shrink:x + w - shrink]

        # Add padding to the letter image
        padding = 0
        letter_image = cv2.copyMakeBorder(letter_image, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # Resize the letter image to a fixed size (e.g., 28x28 pixels) to standardize input for OCR
        letter_image = cv2.resize(letter_image, (28, 28))

        # Use Tesseract to recognize the letter
        letter = pytesseract.image_to_string(letter_image, config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZo')
        recognized_letters.append(letter.strip().lower())
        grid_order.append([(x + 50)//400, (y + 50)//400])

        # Draw the bounding box and recognized letter on the original image (for visualization purposes)
        cv2.rectangle(image, (x + shrink, y + shrink), (x + w - shrink, y + h - shrink), (0, 255, 0), 2)
        cv2.putText(image, letter.strip(), (x + shrink + 10, y + shrink + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


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

