import cv2
import numpy as np
import pytesseract

# Load the image
image = cv2.imread('letters.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)

# Apply thresholding to get a binary image
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Find contours in the binary image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    rect = cv2.boundingRect(c)
    if rect[2] < 100 or rect[3] < 100: continue
    print(cv2.contourArea(c))
    x,y,w,h = rect
    cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),2)

    roi = gray[y:y + h, x:x + w]
    letter = pytesseract.image_to_string(roi, config='--psm 10').strip()
    if letter:
        cv2.putText(thresh, letter, (x + w + 10, y + h), 0, 0.3, (0, 255, 0))
        print(letter)

cv2.imshow('thresh', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
