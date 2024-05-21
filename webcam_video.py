import cv2

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()

    # crop image
    height, width, _ = frame.shape
    frame = frame[0:height - 200, 250:width - 250]

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()