import numpy as np
import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("http://192.168.1.64:8080/video")
while(True):
    frame = cap.read()

    gray = cv2.cvtColor(frame[1], cv2.COLOR_BGR2GRAY)

    blurred = cv2.medianBlur(gray, 25) #cv2.bilateralFilter(gray,10,50,50)
    #blurred = cv2.medianBlur(gray, 25) #cv2.bilateralFilter(gray,10,50,50)

    minDist = 100
    param1 = 30 #500
    param2 = 50 #200 #smaller value-> more false circles
    minRadius = 2
    maxRadius = 100 #10

    # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(blurred, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.imshow('video',blurred)
    if cv2.waitKey(1)==27:# esc Key
        break

cap.release()
cv2.destroyAllWindows()
