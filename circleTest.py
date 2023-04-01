import array
import sys
import cv2 as cv
import numpy as np
from math import ceil, atan2
import util as u
import copy
import encodeUtil as en

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
            circles = np.uint16(np.around(circles))
            finderPatterns = []

            # Check if found circles are finder patterns
            for i in circles[0, :]:

                #i -> (x, y, radius)
                center = (i[0], i[1])
               
                patFinder = u.processPoint(processedImage, i)
                if patFinder is None:
                    continue

                # Old circle center and circumference
                cv.circle(src, center, 1, (0, 0, 255), 3)
                cv.circle(src, center, i[2], (0, 0, 255), 3)

                finderPatterns.append(patFinder[0])

                # Circle aligned center
                # cv.circle(src, patFinder[0], 1, (0, 255, 0), 3)
                # cv.circle(src, patFinder[0], patFinder[1]//2, (0, 255, 0), 3)

            cv.putText(src, f"Valid circles: {len(finderPatterns)}/{circles.size/3}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            if len(finderPatterns) == 4:
                # (x, y)
                sqrCenter = u.getCenter(finderPatterns)

                # cv.circle(src, sqrCenter, 1, (0, 255, 0), 3)
                
                # (x, y)
                # Absolute position of corners to be transformed
                corners = []
                for i in range(0, len(finderPatterns), 1):
                    cornerEst = u.extendPoint(finderPatterns[i], sqrCenter, 1.3 )
                    newPos = finderPatterns[i]
                    if not u.checkBounds(cornerEst, src):
                        break
                    corners.append(newPos)

                if len(corners) == 4:
                    print("\nEVALUATING NEW THINGS -----")
                    

                    corners = sorted(corners, key=lambda c1: u.calcAngle((c1[0], c1[1]), sqrCenter))
                    floatCorners = np.float32(corners)

                    # gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
                    final = u.transformImage(floatCorners, original)
                    final = cv.cvtColor(final, cv.COLOR_BGR2GRAY)
                    final = cv.flip(final, 0)
                    readCorrect = en.readImage(final)

                    if(readCorrect):
                        paused = True
                        cv.imshow("Output", final)
                        cv.imwrite("out.png", final)

                        # for i in range(len(corners)):
                            # cv.circle(src, corners[i], 5, (0, 0, 255), 3)
                            # cv.putText(src, f"{i}", corners[i], cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                            # i += 1



        cv.imshow("detected circles", src)
    if cv.waitKey(1)==27:
        break
cap.release()
cv.destroyAllWindows()

