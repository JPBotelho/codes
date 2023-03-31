from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
SIZE = 1000
CENTER = (SIZE / 2, SIZE / 2)


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
def drawRegion(angleStart, angleStop, startR, endR, width, color, img):
    slices = splitIntoSlices(startR, endR, width)

    angleAmplitude = angleStop - angleStart
    for slice in slices:
        n = calcN(angleAmplitude, slice, width)
        drawSector(angleStart, angleStop, slice, n, color, img)


def drawSector(angleStart, angleStop, r, n, col, img):    
    amplitude = angleStop - angleStart
    areaPerim = (amplitude / 360) * (2*pi*r)
    circleRadius = (areaPerim / n) / 2
    step = amplitude / (2 * n)
    angle = angleStart + step
    #step = (r * 2 * 360) / ( 2 * pi * d *1000)
    print(step) 
    while angle < angleStop:
        en.drawCircle(angle, r, circleRadius, col, img)
        en.drawCircle(angle, r, 2, (0, 0, 0), img1)
        angle += step * 2
        global accum
        accum +=1
accum = 0
#img = Image.new("RGB", (1000, 1000), color=(255, 255, 255))
img = Image.open("uff.png", mode="r", formats=None)
img1 = ImageDraw.Draw(img)

r = 125
color = (0, 0, 0)
# drawSector(0, 360, 270, 90*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 285, 96*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 300, 102*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 315, 108*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 330, 114*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 345, 120*1.5, (255, 0, 100), img1)

drawRegion(60, 122, 262, 365, 15, (255, 0, 0), img1)
drawRegion(150, 212, 262, 365, 15, (255, 0, 0), img1)
drawRegion(330, 392, 262, 365, 15, (255, 0, 0), img1)
drawRegion(240, 302, 262, 365, 15, (255, 0, 0), img1)
shapeUp = [(500, 500), (500, 0)]
shapeLeft = [(500, 500), (0, 500)]
#img1.line(shapeUp, fill="red", width = 0)
#img1.line(shapeLeft, fill="red", width = 0)
print(f"Drew {accum} circles")
# drawCircle(45, 0.2, 15, img1, (255, 0, 255))
# drawCircle(45, 0.6, 15, img1, (255, 0, 255))
#img1.ellipse((x-r, y-r, x+r, y+r), fill=(255, 255, 255))
img.show()