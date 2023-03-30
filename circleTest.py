import array
import sys
import cv2 as cv
import numpy as np
from math import ceil 
def getCenter(points):
    xAcc = 0
    yAcc = 0
    for point in points:
        xAcc += point[0][0]
        yAcc += point[0][1]
    
    count = len(points)

    return (xAcc // count, yAcc // count)

def extendPoint(finderPattern, center, magnitude):
    vx = finderPattern[0] - center[0]
    vy = finderPattern[1] - center[1]
    return (int(center[0] + vx * magnitude), int(center[1] + vy * magnitude))

def checkRatio(stateCount):
    totalSize = 0
    for count in stateCount:
        totalSize += count
        if count == 0:
            return False
    if totalSize < 7:
        return False

    moduleSize = ceil(totalSize / 7.0)
    maxVariance = moduleSize // 2

    val = ((abs(moduleSize - (stateCount[0])) < maxVariance) and
        (abs(moduleSize - (stateCount[1])) < maxVariance) and
        (abs(2.5*moduleSize - (stateCount[2])) < 2.5*maxVariance) and
        (abs(moduleSize - (stateCount[3])) < maxVariance) and
        (abs(moduleSize - (stateCount[4])) < maxVariance))
    
    return val

def centerFromEnd(stateCount, end):
    return end - stateCount[4] - stateCount[3] - (stateCount[2] / 2.0)

def verifyHorizontal(gray, center):
    rows = gray.shape[0]
    cols = gray.shape[1]
    stateCount = [0, 0, 0, 0, 0]

    # Paint original center
    # image[center[1]][center[0]] = (0, 0, 255)
    if(center[1] >= rows):
        return None
    row = gray[center[1]]
    col = center[0]
    
    ##################
    # Traverse to the left

    # Still in black center (state 2)
    while(col >= 0 and row[col] < 128):
        stateCount[2] += 1
        col -= 1

    if(col < 0):
        return None

    while(col >= 0 and row[col] > 128):
        stateCount[1] += 1
        col -= 1

    if(col < 0):
        return None

    while(col >= 0 and row[col] < 128):
        stateCount[0] += 1
        col -= 1
    
    if(col < 0):
        return None

    #############
    # Traverse to the right
    col = center[0]
    while(col < cols and row[col] < 128):
        stateCount[2] += 1
        col += 1
    if(col == cols):
        return None
    while(col < cols and row[col] > 128):
        stateCount[3] += 1
        col += 1
    if(col == cols):
        return None
    while(col < cols and row[col] < 128):
        stateCount[4] += 1
        col += 1

    if(col == cols):
        return None

    if(checkRatio(stateCount)):        
        newCenter = ceil(centerFromEnd(stateCount, col))
        # image[center[1]][newCenter] = (255, 255, 255)
        return (newCenter, center[1])
        #return (newCenter, center[1])
    else:
        return None    

def verifyVertical(gray, center):
    rows = gray.shape[0]
    cols = gray.shape[1]
    stateCount = [0, 0, 0, 0, 0]

    # Paint original center
    # image[center[1]][center[0]] = (0, 0, 255)
    
    row = center[1]
    col = center[0]
    
    ##################
    # Traverse down

    # Still in black center (state 2)
    while(row >= 0 and gray[row][col] < 128):
        stateCount[2] += 1
        row -= 1

    if(row < 0):
        return None

    while(row >= 0 and gray[row][col] > 128):
        stateCount[1] += 1
        row -= 1

    if(row < 0):
        return None

    while(row >= 0 and gray[row][col] < 128):
        stateCount[0] += 1
        row -= 1
    
    if(row < 0):
        return None

    #############
    # Traverse up
    row = center[1]
    while(row < rows and gray[row][col] < 128):
        stateCount[2] += 1
        row += 1
    if(row == rows):
        return None
    while(row < rows and gray[row][col] > 128):
        stateCount[3] += 1
        row += 1
    if(row == rows):
        return None
    while(row < rows and gray[row][col] < 128):
        stateCount[4] += 1
        row += 1

    if(row == rows):
        return None

    if(checkRatio(stateCount)):        
        newCenter = ceil(centerFromEnd(stateCount, row))
        
        totalSize = 0
        for state in stateCount:
            totalSize += state
        # image[center[1]][newCenter] = (255, 255, 255)
        #return (newCenter, center[0])
        return ((center[0], newCenter), totalSize)
    else:
        return None 

cap = cv.VideoCapture(0)
paused = False
possibleCenters = []
while(True):
    if(cv.waitKey(1) == 9) and paused:
        paused = False
    if not paused:
        src = cap.read()[1]
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        thres = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 51, 0)

        gray = thres
        gray = cv.medianBlur(gray, 5)
        

        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                                    param1=100, param2=30,
                                    minRadius=1, maxRadius=60)


    if circles is not None and circles.size >= 3 * 3:
        if(cv.waitKey(1) == 9) and not paused:
            paused = True
            for c in circles[0, :]:
                    possibleCenters.append((c[0], c[1]))

    if not paused:
        if circles is not None:
            totalCircles = circles.size / 3
            circles = np.uint16(np.around(circles))
            finderPatterns = []
            for i in circles[0, :]:
                center = (i[0], i[1])
                
                horCenter = verifyHorizontal(gray, center)

                if horCenter is None:
                    totalCircles -= 1
                    continue

                newCenter = verifyVertical(gray, horCenter)

                if newCenter is None:
                    totalCircles -= 1
                    continue

                # circle center
                cv.circle(src, center, 1, (0, 0, 255), 3)
                # circle outline
                radius = i[2]
                cv.circle(src, center, radius, (0, 0, 255), 3)
                finderPatterns.append(newCenter)
                # circle new center
                cv.circle(src, newCenter[0], 1, (0, 255, 0), 3)
                cv.circle(src, newCenter[0], newCenter[1]//2, (0, 255, 0), 3)
            cv.putText(src, f"Valid circles: {totalCircles}/{circles.size/3}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if totalCircles == 4:
                paused = True
                sqrCenter = getCenter(finderPatterns)

                cv.line(src, finderPatterns[3][0], finderPatterns[0][0], (0, 0, 255), 3)
                for i in range(0, len(finderPatterns), 1):
                    newPos = extendPoint(finderPatterns[i][0], sqrCenter, 1.75)
                    cv.circle(src, newPos, 15, (0, 0, 255), 3)
                    # cv.line(src, finderPatterns[i][0], finderPatterns[i+1][0], (0, 0, 255), 3)
                cv.circle(src, sqrCenter, 15, (0, 0, 255), 3)


        cv.imshow("detected circles", src)
    if cv.waitKey(1)==27:
        break
cap.release()
cv.destroyAllWindows()

