SIZE = 1000
CENTER = (SIZE // 2, SIZE // 2)

from math import cos, sin, pi
import numpy as np 
DATA_STRING = "HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD!"
DATA = []

INDEX = 0

COLOR_YES = (0, 0, 0)
COLOR_NO = (255, 255, 255)

def init_data():
    for c in DATA_STRING:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        DATA.extend([int(b) for b in bits])
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
    global INDEX, COLOR_NO, COLOR_YES, DATA      
    a = toRad(angle)
    dist = d
    c = toCart(a, dist, CENTER)
    if INDEX < len(DATA) and enc:
        bit = DATA[INDEX]
        if bit == 0:
            col = COLOR_NO
        else:
            col = COLOR_YES
        INDEX += 1
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


def drawSector(angleStart, angleStop, r, n, col, img):    
    amplitude = angleStop - angleStart
    areaPerim = (amplitude / 360) * (2*pi*r)
    circleRadius = (areaPerim / n) / 2
    step = amplitude / (2 * n)
    angle = angleStart + step
    #step = (r * 2 * 360) / ( 2 * pi * d *1000)
    print(step) 
    while angle < angleStop:
        drawCircle(angle, r, circleRadius, col, img, True)
        # drawCircle(angle, r, 2, (0, 0, 0), img, False)
        angle += step * 2

def calcAngles(center, amplitude):
    return (center - amplitude // 2, center + amplitude // 2)
        