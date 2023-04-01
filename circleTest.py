import array
import sys
import cv2 as cv
import numpy as np
from math import ceil, atan2
import util as u
import copy

cap = cv.VideoCapture(0)
paused = False

while(True):
    if(cv.waitKey(1) == 9) and paused:
        paused = False
    if not paused:
        src = cap.read()[1]
        original = copy.deepcopy(src)
        processedImage = u.processImage(src)
        rows = processedImage.shape[0]
        circles = cv.HoughCircles(processedImage, cv.HOUGH_GRADIENT, 1, rows / 8,
                                    param1=100, param2=30,
                                    minRadius=1, maxRadius=60)

        if circles is not None and circles.size / 3 >= 4:
            totalCircles = circles.size / 3
            circles = np.uint16(np.around(circles))
            finderPatterns = []

            # Check if found circles are finder patterns
            for i in circles[0, :]:

                #i -> (x, y, radius)
                center = (i[0], i[1])
               
                patFinder = u.processPoint(processedImage, i)
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
                cv.circle(src, sqrCenter, 1, (0, 255, 0), 3)
                # (x, y)
                # Absolute position of corners to be transformed
                corners = []
                cornerArr = []
                for i in range(0, len(finderPatterns), 1):
                    # newPos = u.extendPoint(finderPatterns[i], sqrCenter, 1.7)
                    cornerEst = u.extendPoint(finderPatterns[i], sqrCenter, 1.7 )
                    newPos = finderPatterns[i]
                    if not u.checkBounds(cornerEst, src):
                        break
                        
                    # Position of corner relative to center.
                    cornerArr.append([newPos[0], newPos[1]])
                    corners.append(newPos)
                if len(corners) == 4:
                    paused = True
                    cornerArr = sorted(cornerArr, key=lambda c1: u.calcAngle((c1[0], c1[1]), sqrCenter))
                    corners = sorted(corners, key=lambda c1: u.calcAngle(c1, sqrCenter))
                    cornerArr = np.float32(cornerArr)
                    #startPos = np.float32(corners)
                    es = 222#//2
                    l = 1000#//2
                    targetRect = np.float32([[0+es, l-es], [l-es, l-es], [l-es, 0+es], [0+es, 0+es]])
                    m = cv.getPerspectiveTransform(cornerArr, targetRect)
                    final = cv.warpPerspective(original, m, (l, l), cv.INTER_NEAREST)
                    cv.imshow("Output", final)
                    final = cv.flip(final, 0)
                    cv.imwrite("out.png", final)
                    ind = 0
                    for corner in corners:
                        cv.circle(src, corner, 5, (0, 0, 255), 3)
                        cv.putText(src, f"{ind}", corner, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        ind += 1
                    


        cv.imshow("detected circles", src)
    if cv.waitKey(1)==27:
        break
cap.release()
cv.destroyAllWindows()

