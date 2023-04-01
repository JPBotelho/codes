from math import ceil, atan2
import cv2 as cv 
import numpy as np
# Returns center of list of FinderPattern (x, y)
def getCenter(points):
    xAcc = 0
    yAcc = 0
    for point in points:
        xAcc += point[0]
        yAcc += point[1]
    
    count = len(points)

    return (xAcc // count, yAcc // count)

# Returns new point (x, y)
def extendPoint(finderPattern, center, magnitude):
    vx = finderPattern[0] - center[0]
    vy = finderPattern[1] - center[1]
    return (int(center[0] + vx * magnitude), int(center[1] + vy * magnitude))


def checkBounds(point, image):
    if point[0] <= 0 or point[1] <= 0:
        return False
    
    if point[0] >= image.shape[1]:
        return False

    if point[1] >= image.shape[0]:
        return False

    return True

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

def alignHorizontal(gray, center):
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

def alignVertical(gray, center):
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


def processImage(src):
    image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 51, 0)
    image = cv.medianBlur(image, 5)
    return image

def processPoint(image, point):
    # Horizontally aligned center
    # (x, y)
    horCenter = alignHorizontal(image, point)

    if horCenter is None:
        return None

    # Vertically aligned center and diameter
    # (x, y, pattern diameter)
    patFinder = alignVertical(image, horCenter)

    return patFinder

def calcAngle(point, center):
    y = point[1] - center[1]
    x = point[0] - center[0]
    return atan2(y, x)

def transformImage(finderPatterns, image):
    pc = 222#//2
    l = 1000#//2
    targetRect = np.float32([[pc, l-pc], [l-pc, l-pc], [l-pc, pc], [pc, pc]])

    m = cv.getPerspectiveTransform(finderPatterns, targetRect)

    result = cv.warpPerspective(image, m, (l, l), cv.INTER_NEAREST)

    return result