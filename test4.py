from math import ceil
import cv2 as cv
import numpy as np
import time
imageCopy = cv.imread("test.jpg")
#imageCopy = cv.imread("test.png")
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
        (abs(3*moduleSize - (stateCount[2])) < 3*maxVariance) and
        (abs(moduleSize - (stateCount[3])) < maxVariance) and
        (abs(moduleSize - (stateCount[4])) < maxVariance))
    
    return val

def findPatterns(image):
    possibleCenters = []
    rows = image.shape[0]
    cols = image.shape[1]
    cv.circle(imageCopy, (50, 200), 30, (255, 0, 255))
    imageCopy[50][200] = (255, 0, 255)
    for r in range(0, rows, 3):
        stateCount = [0, 0, 0, 0, 0]
        currentState = 0
        row = image[r]
        #print(image.shape[1])
        temp = []
        c = 0
        for c in range(cols):
            if(currentState == 0 and stateCount[0] == 0):
                temp = [r, c]
            if(row[c] < 128):
                # Counting white pixels
                # (States 1 and 3)
                # ->Change to next state
                if currentState % 2 == 1:
                    currentState += 1
                stateCount[currentState] += 1
            
            # White pixel
            else:
                # Counting White pixels
                # ->(just increment)
                if currentState % 2 == 1:
                    stateCount[currentState] += 1
                else:
                    if currentState == 4:
                    # Travelled all states, need to test validity
                        if(checkRatio(stateCount)):
                            possibleCenters.append((r, c))
                            
                            #imageCopy[t[0]][t[1]] = (0, 0, 255)
                            cv.circle(imageCopy, (temp[1], temp[0]), 3, (0, 0, 255))

                            cv.circle(imageCopy, (c, r), 3, (255, 0, 255))

                            temp = []
                            stateCount = [0, 0, 0, 0, 0]
                            currentState = 0
                            #imageCopy[r][c] = (0, 0, 255)
                            #image[r][c] = 100
                            #print("Found possible match")
                        else:
                            #temp = []
                        # Travelled pixels are not valid. Shift parts.
                            currentState = 3
                            stateCount[0] = stateCount[2]
                            stateCount[1] = stateCount[3]
                            stateCount[2] = stateCount[4]
                            stateCount[3] = 1
                            stateCount[4] = 0
                            temp = [r, c]
                            continue
                        currentState = 0
                        stateCount = [0, 0, 0, 0, 0]
                    elif currentState == 0 and stateCount[0] == 0:
                        continue
                    else:
                        # We are leaving state 0 or 2
                        currentState += 1
                        stateCount[currentState] += 1
        #print(f"Row #{c}")
    print(f"Found {len(possibleCenters)}")
    return

#frame = cv.imread("test.png", cv.IMREAD_GRAYSCALE)  
frame = cv.imread("test.jpg", cv.IMREAD_GRAYSCALE)  
#rframe = cv.bitwise_not(frame)
cv.imshow("Filtering Circular Blobs eeOnly", frame)

startTime = time.time()
findPatterns(frame)
elapsed = time.time() - startTime
print(f"Finished in {elapsed}s")

cv.imshow("Filtering Circular Blobs Only", imageCopy)
#cv.imshow("Filtering Circular Blobs Only", imageCopy)

cv.waitKey(0)

# Show blobs
cv.destroyAllWindows()


