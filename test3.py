import cv2
import numpy as np
import sys
cap = cv2.VideoCapture(0)
while(True):
    frame = cap.read()
    gray = cv2.medianBlur(cv2.cvtColor(frame[1], cv2.COLOR_BGR2GRAY),5)
    
    cv2.imshow('video',frame[1])
    if cv2.waitKey(1)==27:# esc Key
        break
cap.release()
cv2.destroyAllWindows()
