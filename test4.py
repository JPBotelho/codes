import cv2 as cv
import numpy as np
  
def checkRatio(stateCount):
    return False

def findPatterns(image):
    possibleCenters = []
    rows = image.shape[0]
    cols = image.shape[1]

    for r in range(rows):
        stateCount = {0, 0, 0, 0, 0}
        currentState = 0
        row = image[r]
        #print(image.shape[1])
        for c in range(cols):
            # Black Pixel
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
                elif currentState == 4:
                    # Travelled all states, need to test validity
                    if(checkRatio(stateCount)):
                        possibleCenters.append()
                        continue
                    else:
                    # Travelled pixels are not valid. Shift parts.
                        currentState = 3
                        stateCount[0] = stateCount[2]
                        stateCount[1] = stateCount[3]
                        stateCount[2] = stateCount[4]
                        stateCount[3] = 1
                        stateCount[4] = 0
                        continue
                else:
                    # We are leaving state 0 or 2
                    currentState += 1
                    stateCount[currentState] += 1
        #print(f"Row #{c}")
    return

frame = cv.imread("test.png", cv.IMREAD_GRAYSCALE)  
frame = cv.bitwise_not(frame)
findPatterns(frame)

cv.imshow("Filtering Circular Blobs Only", frame)
cv.waitKey(0)

# Show blobs
cv.destroyAllWindows()


