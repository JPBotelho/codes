import array
import sys
import cv2 as cv
import numpy as np
from math import ceil, atan2
import util as u


cap = cv.VideoCapture(0)
paused = False
possibleCenters = []
while(True):
    if(cv.waitKey(1) == 9) and paused:
        paused = False
    if not paused:
        src = cap.read()[1]
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        gray = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 51, 0)
        gray = cv.medianBlur(gray, 5)
        
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                                    param1=100, param2=30,
                                    minRadius=1, maxRadius=60)

    if not paused:
        if circles is not None and circles.size / 3 >= 4:
            totalCircles = circles.size / 3
            circles = np.uint16(np.around(circles))
            finderPatterns = []

            # Check if found circles are finder patterns
            for i in circles[0, :]:

                #i -> (x, y, radius)
                center = (i[0], i[1])
                
                # Horizontally aligned center
                # (x, y)
                horCenter = u.alignHorizontal(gray, center)

                if horCenter is None:
                    totalCircles -= 1
                    continue

                # Vertically aligned center and diameter
                # (x, y, pattern diameter)
                patFinder = u.alignVertical(gray, horCenter)

                if patFinder is None:
                    totalCircles -= 1
                    continue

                # Old circle center and circumference
                cv.circle(src, center, 1, (0, 0, 255), 3)
                cv.circle(src, center, i[2], (0, 0, 255), 3)

                finderPatterns.append(patFinder[0])

                # Circle aligned center
                cv.circle(src, patFinder[0], 1, (0, 255, 0), 3)
                cv.circle(src, patFinder[0], patFinder[1]//2, (0, 255, 0), 3)

            cv.putText(src, f"Valid circles: {totalCircles}/{circles.size/3}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            if totalCircles == 4:
                # (x, y)
                sqrCenter = u.getCenter(finderPatterns)
                corners = []
                for i in range(0, len(finderPatterns), 1):
                    newPos = u.extendPoint(finderPatterns[i], sqrCenter, 1.75)
                    if not u.checkBounds(newPos, src):
                        break
                        
                    corners.append(newPos)
                if len(corners) == 4:
                    paused = True
                    for corner in corners:
                        cv.circle(src, corner, 5, (0, 0, 255), 3)



        cv.imshow("detected circles", src)
    if cv.waitKey(1)==27:
        break
cap.release()
cv.destroyAllWindows()

