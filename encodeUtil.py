SIZE = 1000
CENTER = (SIZE // 2, SIZE // 2)

from math import cos, sin, pi
import numpy as np 
DATA_STRING = "HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD!"
WRITE_DATA = []

WRITE_INDEX = 0
READ_INDEX = 0
READ_BYTES = []
CURR_BYTE = []

COLOR_YES = (0, 0, 0)
COLOR_NO = (255, 255, 255)

def init_data():
    for c in DATA_STRING:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        WRITE_DATA.extend([int(b) for b in bits])
    # print (DATA)
def circle(imgDraw, center, r, color):
    x = center[0]
    y = center[1]
    imgDraw.ellipse((x-r, y-r, x+r, y+r), fill=color)

def toCart(angle, dist, center):
    x = dist * cos(angle)
    y = dist * sin(angle)
    return (x + center[0], y + center[1])

def toRad(angle):
    return (angle * -2*pi) / 360

def drawCircle(position, r, col, img, enc):  
    global WRITE_INDEX, COLOR_NO, COLOR_YES, WRITE_DATA      

    if WRITE_INDEX < len(WRITE_DATA) and enc:
        bit = WRITE_DATA[WRITE_INDEX]
        if bit == 0:
            col = COLOR_NO
        else:
            col = COLOR_YES
        WRITE_INDEX += 1
    circle(img, position, r, col)

    


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
    global CURR_BYTE, READ_BYTES, READ_INDEX
    amplitude = angleStop - angleStart
    step = amplitude / (2 * n)
    angle = angleStart + step

    positions = [] 
    while angle < angleStop:
        pos = toCart(toRad(angle), dist, CENTER)
        positions.append(pos)
        angle += step * 2
    return positions
    

def calcAngles(center, amplitude):
    return (center - amplitude // 2, center + amplitude // 2)
        
def readPos(center, radius, img):
    global CURR_BYTE, READ_BYTES, READ_INDEX

    accum = 0
    iter = 0
    radius = int(radius)
    for x in range(-radius, radius):
        accum += img.getpixel((center[0]+x, center[1]))[0]
        accum += img.getpixel((center[0], center[1]+x))[0]
        iter+=2

    val = (accum / iter) < 128

    numVal = int(val)

    READ_INDEX += 1
    if(len(CURR_BYTE) == 8):
        byteStr = "".join(str(b) for b in CURR_BYTE[::])
        intVal = int(byteStr, 2)
        c = chr(intVal)
        READ_BYTES.append(c)
        CURR_BYTE = []
    CURR_BYTE.append(numVal)


def readRegion(angleAmplitude, angleMiddle, startR, endR, width, img):
    slices = splitIntoSlices(startR, endR, width)

    angleStop = angleMiddle + angleAmplitude // 2
    angleStart = angleMiddle - angleAmplitude // 2
    # angleAmplitude = angleStop - angleStart
    for slice in slices:
        n = calcN(angleAmplitude, slice, width)
        drawPositions = getPositionsInSlice(angleStart, angleStop, slice, n)
        for pos in drawPositions:
            readPos(pos, width, img)
            #drawCircle(pos, 2, (255, 0, 0), img, False)
        # drawSector(angleStart, angleStop, slice, n, color, img, False)
    print(READ_BYTES)
    print(READ_INDEX)
