from math import ceil

def centerFromEnd(stateCount, end):
    return end - stateCount[4] - stateCount[3] - (stateCount[2] / 2.0)

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

# Circle = (x, y, radius)
def finderPatterns(image, circles):
    if circles is None:
        return None
    
    out = []
    for circle in circles[0, :]:
        center = (circle[0], circle[1])
        processedPoint = processPoint(image, circle)
        
        if processedPoint is not None:
           out.append(processedPoint)  
    return out
    