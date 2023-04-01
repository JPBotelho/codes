from math import cos, sin, pi
import numpy as np 
import cv2 as cv
SIZE = 1000
CENTER = (SIZE // 2, SIZE // 2)

COLOR_YES = (0, 0, 0)
COLOR_NO = (255, 255, 255)

def toCart(angle, dist, center):
    x = dist * cos(angle)
    y = dist * sin(angle)
    return (x + center[0], y + center[1])

def toRad(angle):
    return (angle * -2*pi) / 360

def circle(imgDraw, center, r, color):
    x = center[0]
    y = center[1]
    imgDraw.ellipse((x-r, y-r, x+r, y+r), fill=color)

# Outputs array with values of R, one for each slice. 
def splitIntoSlices(startR, endR, bitWidth):
    amplitude = endR - startR
    n = amplitude // bitWidth
    stepSize = bitWidth / 2

    slices = []
    firstPos = startR + stepSize
    slices.append(firstPos)
    for i in range(n - 1):
        firstPos += bitWidth
        slices.append(firstPos)

    return slices

# Calculate N given the amplitude and radius
# r must be absolute!!
def calcN(amplitude, distance, bitWidth):
    slicePerimeter = (amplitude / 360) * (2 * pi * distance)
    n = slicePerimeter // bitWidth
    return n


def getPositionsInSlice(angleStart, angleStop, dist, n):    
    amplitude = angleStop - angleStart
    step = amplitude / (2 * n)
    angle = angleStart + step

    positions = [] 
    while angle < angleStop:
        pos = toCart(toRad(angle), dist, CENTER)
        positions.append(pos)
        angle += step * 2
    return positions

# Encodes given set of points with given data based on YES/NO global color.
def encodePoints(points, data, width, imgDraw):
    if(len(data) != len(points)):
        print("Number of points to encode doesn't match size of data!")
        return
    for i in range(len(points)):
        point = points[i]
        bit = data[i]
        color = COLOR_NO
        if(bit == 1):
            color = COLOR_YES
        circle(imgDraw, point, width / 2, color)

# Returns array with the center position of all the points in a region
def getPointsInRegion(angleAmplitude, angleMiddle, startR, endR, width):
    slices = splitIntoSlices(startR, endR, width)

    angleStop = angleMiddle + angleAmplitude // 2
    angleStart = angleMiddle - angleAmplitude // 2

    positionsInRegion = []
    for slice in slices:
        n = calcN(angleAmplitude, slice, width)
        positionsInSlice = getPositionsInSlice(angleStart, angleStop, slice, n)

        for pos in positionsInSlice:
            positionsInRegion.append(pos)
    return positionsInRegion
    
# Calculates startAngle and endAngle given a center angle and an amplitude
def calcAngles(center, amplitude):
    return (center - amplitude // 2, center + amplitude // 2)
        

def readPosCV(center, radius, img, thres):
    ic = [int(center[0]), int(center[1])]

    accum = 0
    iter = 0
    radius = radius // 2
    radius = int(radius)
    for x in range(-radius, radius):
        accum += img[ic[1]+x, ic[0]]
        accum += img[ic[1], ic[0]+x]
        iter+=2

    val = (accum / iter) < thres
    
    numVal = int(val)
    col = (255)
    if(numVal == 1):
        col = (0)
    # cv.circle(img, ic, 2, col, 1)
    return numVal

def readPos(center, radius, img, thres):
    accum = 0
    iter = 0
    radius = radius // 2
    radius = int(radius)
    for x in range(-radius, radius):
        accum += img.getpixel((center[0]+x, center[1]))
        accum += img.getpixel((center[0], center[1]+x))#[0]
        iter+=2

    val = (accum / iter) < thres
    
    numVal = int(val)
    return numVal

def readPositions(positions, width, img, opencv, imgdraw):
    currByte = []
    bits90 = []
    bits120 = []
    bits150 = []

    outputString = ""
    for pos in positions:
        
        bit = None
        if opencv:
            bit90 = readPosCV(pos, width, img, 90)
            bit120 = readPosCV(pos, width, img, 120)
            bit150 = readPosCV(pos, width, img, 150)
        else:
            bit90 = readPos(pos, width, img, 90)
            bit120 = readPos(pos, width, img, 120)
            bit150 = readPos(pos, width, img, 150)

        bits90.append(bit90)
        bits120.append(bit120)
        bits150.append(bit150)

        #if(len(currByte) == 8):
        #    byteStr = "".join(str(b) for b in currByte[::])
        #    intVal = int(byteStr, 2)
        #    c = chr(intVal)
        #    outputString += c
        #    currByte = []
        #currByte.append(bit)

        if(imgdraw is not None):
            if(bit150 == 1):
                circle(imgdraw, pos, 2, (200))
            else:
                circle(imgdraw, pos, 2, (100))

    return (bits90, bits120, bits150)
    #return outputString

# Converts characters from str to their binary representation
# If string runs out or size is not multiple of 8, 
# Pads the end with zeros.
# Returns array with individual bits (0, 1)
def strToBitArray(str, size):
    output = []
    charIndex = 0 
    while(len(output) + 8 <= size):
        if(charIndex >= len(str)):
            break
        c = str[charIndex]
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        output.extend([int(b) for b in bits])
        charIndex += 1
    while(len(output) < size):
        output.append(0)
    return output


def checkValidity(original, data):
    if(len(original) != len(data)):
        print(f"\nLength of data does not match! (Original = {len(original)}, Data = {len(data)}")
        return 

    # print("\n"+original)
    # print(data)
    
    matches = 0
    for i in range(len(data)):
        if(original[i] == data[i]):
            matches += 1
            
    validity = (matches / len(data)) * 100
    # print(f"{validity}% match!\n")

    return validity

def bitArrayToString(data):
    currByte = []
    output = ""

    for i in range(len(data)):
        if len(currByte) == 8:
            byteStr = "".join(str(b) for b in currByte[::])
            intVal = int(byteStr, 2)
            c = chr(intVal)
            output += c
            currByte = []
        currByte.append(data[i])
    return output

def readImage(image):
    DATA_STRING = "HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD!"
    WRITE_BITS = strToBitArray(DATA_STRING, 50)
    ENCODED_STRING = bitArrayToString(WRITE_BITS)

    minDist = 325
    maxDist = 465
    amplitude = 65

    reg1 = getPointsInRegion(amplitude, 90, minDist, maxDist, 35)
    reg2 = getPointsInRegion(amplitude, 0, minDist, maxDist, 35)
    reg3 = getPointsInRegion(amplitude, 180, minDist, maxDist, 35)
    reg4 = getPointsInRegion(amplitude, 270, minDist, maxDist, 35)

    readSectors = []
    secondaryReadSectors = []
    thirdSectors = []

    res = readPositions(reg1, 15, image, True, None)
    readSectors.append(res[0])
    secondaryReadSectors.append(res[1])
    thirdSectors.append(res[2])

    res = readPositions(reg2, 15, image, True, None)
    readSectors.append(res[0])
    secondaryReadSectors.append(res[1])
    thirdSectors.append(res[2])

    res = readPositions(reg3, 15, image, True, None)
    readSectors.append(res[0])
    secondaryReadSectors.append(res[1])
    thirdSectors.append(res[2])

    res = readPositions(reg4, 15, image, True, None)
    readSectors.append(res[0])
    secondaryReadSectors.append(res[1])
    thirdSectors.append(res[2])

    ret = True
    
    goodSectors = 4
    for i in range(len(readSectors)):
        readString = bitArrayToString(readSectors[i])
        validity = checkValidity(ENCODED_STRING, readString)

        secondString = bitArrayToString(secondaryReadSectors[i])
        secondValidity = checkValidity(ENCODED_STRING, secondString)

        thirdString = bitArrayToString(thirdSectors[i])
        thirdValidity = checkValidity(ENCODED_STRING, thirdString)

        maxVal = max(validity, secondValidity, thirdValidity)
        print(f"Sector {i}: {maxVal}%")

        if(maxVal < 90):
            #continue
            ret = False
    return ret
