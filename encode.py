from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
import numpy as np 
import random as rnd
SIZE = 1000
CENTER = (SIZE / 2, SIZE / 2)

DATA_STRING = "HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD!"
WRITE_BITS = []

WRITE_BITS = en.strToBitArray(DATA_STRING, 283)

img = Image.open("test.png", mode="r", formats=None)
img1 = ImageDraw.Draw(img)
r = 125
color = (0, 0, 0)

minDist = 325
maxDist = 465

regPoints = en.getPointsInRegion(70, 90, minDist, maxDist, 15)
en.encodePoints(regPoints, WRITE_BITS, 15, (255, 0, 0), img1)

regPoints = en.getPointsInRegion(70, 0, minDist, maxDist, 15)
en.encodePoints(regPoints, WRITE_BITS, 15, (255, 0, 0), img1)

regPoints = en.getPointsInRegion(70, 180, minDist, maxDist, 15)
en.encodePoints(regPoints, WRITE_BITS, 15, (255, 0, 0), img1)

regPoints = en.getPointsInRegion(70, 270, minDist, maxDist, 15)
en.encodePoints(regPoints, WRITE_BITS, 15, (255, 0, 0), img1)

scanned = Image.open("out.png", mode="r", formats=None)
# Grayscale
scanned = scanned.convert('L')
# Threshold
#scanned = scanned.point( lambda p: 255 if p > 200 else 0 )
# scanned = scanned.convert('1')
scannedWriter = ImageDraw.Draw(scanned)
out = en.readRegion(70, 90, minDist, maxDist, 15, scanned, scannedWriter)
out += en.readRegion(70, 0, minDist, maxDist, 15, scanned, scannedWriter)
out += en.readRegion(70, 180, minDist, maxDist, 15, scanned, scannedWriter)
out += en.readRegion(70, 270, minDist, maxDist, 15, scanned, scannedWriter)

print(out)
scanned.show()

img.show()