from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
import numpy as np 

SIZE = 1000
CENTER = (SIZE / 2, SIZE / 2)



accum = 0
def drawRegion(angleAmplitude, angleMiddle, startR, endR, width, color, img):
    global accum
    slices = en.splitIntoSlices(startR, endR, width)

    angleStop = angleMiddle + angleAmplitude // 2
    angleStart = angleMiddle - angleAmplitude // 2
    # angleAmplitude = angleStop - angleStart
    for slice in slices:
        n = en.calcN(angleAmplitude, slice, width)
        positionsInSlice = en.getPositionsInSlice(angleStart, angleStop, slice, n)
        #en.drawSector(angleStart, angleStop, slice, n, color, img, True)
        for pos in positionsInSlice:
            en.drawCircle(pos, width/2, color, img, True)
        accum += n





#img = Image.new("RGB", (1000, 1000), color=(255, 255, 255))
img = Image.open("test.png", mode="r", formats=None)
img1 = ImageDraw.Draw(img)
en.init_data()
r = 125
color = (0, 0, 0)

minDist = 325
maxDist = 465

drawRegion(70, 90, minDist, maxDist, 15, (255, 0, 0), img1)
# en.readRegion(70, 90, minDist, maxDist, 16, img)

drawRegion(70, 0, minDist, maxDist, 15, (255, 0, 0), img1)
# en.readRegion(70, 0, minDist, maxDist, 16, img)

drawRegion(70, 180, minDist, maxDist, 15, (255, 0, 0), img1)
# en.readRegion(70, 180, minDist, maxDist, 16, img)

drawRegion(70, 270, minDist, maxDist, 15, (255, 0, 0), img1)
# en.readRegion(70, 270, minDist, maxDist, 16, img)

scanned = Image.open("out.png", mode="r", formats=None)
# Grayscale
scanned = scanned.convert('L')
# Threshold
#scanned = scanned.point( lambda p: 255 if p > 200 else 0 )
# scanned = scanned.convert('1')
scannedWriter = ImageDraw.Draw(scanned)
en.readRegion(70, 90, minDist, maxDist, 15, scanned, scannedWriter)
en.readRegion(70, 0, minDist, maxDist, 15, scanned, scannedWriter)
en.readRegion(70, 180, minDist, maxDist, 15, scanned, scannedWriter)
en.readRegion(70, 270, minDist, maxDist, 15, scanned, scannedWriter)
scanned.show()

print(f"Drew {accum} circles")

img.show()