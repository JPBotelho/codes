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

def drawCircle(angle, d, r, col, img, enc):  
    global WRITE_INDEX, COLOR_NO, COLOR_YES, WRITE_DATA      
    a = toRad(angle)
    dist = d
    c = toCart(a, dist, CENTER)
    if WRITE_INDEX < len(WRITE_DATA) and enc:
        bit = WRITE_DATA[WRITE_INDEX]
        if bit == 0:
            col = COLOR_NO
        else:
            col = COLOR_YES
        WRITE_INDEX += 1
    circle(img, c, r, col)
    


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
def calcN(amplitude, r, bitWidth):
    slicePerimeter = (amplitude / 360) * (2 * pi * r)
    n = slicePerimeter // bitWidth
    return n


def drawSector(angleStart, angleStop, r, n, col, img, write):    
    global CURR_BYTE, READ_BYTES, READ_INDEX
    amplitude = angleStop - angleStart
    areaPerim = (amplitude / 360) * (2*pi*r)
    circleRadius = (areaPerim / n) / 2
    step = amplitude / (2 * n)
    angle = angleStart + step
    #step = (r * 2 * 360) / ( 2 * pi * d *1000)
    #print(step) 
    while angle < angleStop:
        if(write):
            drawCircle(angle, r, circleRadius, col, img, True)
        else:
            pos = toCart(toRad(angle), r, CENTER)
            val = readPos(pos, circleRadius, img)
            READ_INDEX += 1
            if(len(CURR_BYTE) == 8):
                byteStr = "".join(str(b) for b in CURR_BYTE[::])
                intVal = int(byteStr, 2)
                c = chr(intVal)
                READ_BYTES.append(c)
                CURR_BYTE = []
            CURR_BYTE.append(val)
            # readCircle
        # drawCircle(angle, r, 2, (0, 0, 0), img, False)
        angle += step * 2
    if not write:
        print("Wait")

def calcAngles(center, amplitude):
    return (center - amplitude // 2, center + amplitude // 2)
        
def readPos(center, radius, img):
    accum = 0
    iter = 0
    radius = int(radius)
    for x in range(-radius, radius):
        accum += img.getpixel((center[0]+x, center[1]))[0]
        accum += img.getpixel((center[0], center[1]+x))[0]
        iter+=2

    val = (accum / iter) < 128
    if val: 
        return 1
    return 0


def readRegion(angleAmplitude, angleMiddle, startR, endR, width, color, img):
    slices = splitIntoSlices(startR, endR, width)

    angleStop = angleMiddle + angleAmplitude // 2
    angleStart = angleMiddle - angleAmplitude // 2
    # angleAmplitude = angleStop - angleStart
    for slice in slices:
        n = calcN(angleAmplitude, slice, width)
        drawSector(angleStart, angleStop, slice, n, color, img, False)
    print(READ_BYTES)
    print(READ_INDEX)
