from math import ceil, atan2
import cv2 as cv 
import numpy as np
# Returns center of list of FinderPattern (x, y)
def getCenter(points):
    xAcc = 0
    yAcc = 0
    for point in points:
        pos = point[0]
        xAcc += pos[0]
        yAcc += pos[1]
    
    count = len(points)

    return (xAcc // count, yAcc // count)

# Returns new point (x, y)
def extendPoint(finderPattern, center, magnitude):
    pos = finderPattern[0]
    vx = pos[0] - center[0]
    vy = pos[1] - center[1]
    return (int(center[0] + vx * magnitude), int(center[1] + vy * magnitude))


def checkBounds(point, image):
    if point[0] <= 0 or point[1] <= 0:
        return False
    
    if point[0] >= image.shape[1]:
        return False

    if point[1] >= image.shape[0]:
        return False

    return True




def processImage(src):
    image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 51, 0)
    image = cv.medianBlur(image, 5)
    return image

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