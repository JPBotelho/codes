from math import cos, sin, pi
import numpy as np 

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

def encodePoints(points, data, width, color, imgDraw):
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
    

def calcAngles(center, amplitude):
    return (center - amplitude // 2, center + amplitude // 2)
        
def readPos(center, radius, img):
    accum = 0
    iter = 0
    radius = radius // 2
    radius = int(radius)
    for x in range(-radius, radius):
        accum += img.getpixel((center[0]+x, center[1]))
        accum += img.getpixel((center[0], center[1]+x))#[0]
        iter+=2

    val = (accum / iter) < 120
    
    numVal = int(val)
    return numVal

def readPositions(positions, width, img, imgdraw):
    currByte = []
    outputString = ""
    for pos in positions:
        bit = readPos(pos, width, img)

        if(len(currByte) == 8):
            byteStr = "".join(str(b) for b in currByte[::])
            intVal = int(byteStr, 2)
            c = chr(intVal)
            outputString += c
            currByte = []
        currByte.append(bit)

        if(bit == 1):
            circle(imgdraw, pos, 2, (200))
        else:
            circle(imgdraw, pos, 2, (100))

    return outputString

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
    while(len(output) < size):
        output.append(0)
    return output



