from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
import numpy as np 
import random as rnd
import time 

DATA_STRING = "HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD!"
WRITE_BITS = []

WRITE_BITS = en.strToBitArray(DATA_STRING, 283)

img = Image.open("test.png", mode="r", formats=None)
imgDraw = ImageDraw.Draw(img)

minDist = 325
maxDist = 465
amplitude = 70

reg1 = en.getPointsInRegion(amplitude, 90, minDist, maxDist, 15)
reg2 = en.getPointsInRegion(amplitude, 0, minDist, maxDist, 15)
reg3 = en.getPointsInRegion(amplitude, 180, minDist, maxDist, 15)
reg4 = en.getPointsInRegion(amplitude, 270, minDist, maxDist, 15)

en.encodePoints(reg1, WRITE_BITS, 15, imgDraw)
en.encodePoints(reg2, WRITE_BITS, 15, imgDraw)
en.encodePoints(reg3, WRITE_BITS, 15, imgDraw)
en.encodePoints(reg4, WRITE_BITS, 15, imgDraw)

start_time = time.time()

scanned = Image.open("out.png", mode="r", formats=None)
# Grayscale
scanned = scanned.convert('L')
# Threshold
#scanned = scanned.point( lambda p: 255 if p > 200 else 0 )

scannedWriter = ImageDraw.Draw(scanned)

out = en.readPositions(reg1, 15, scanned, scannedWriter)
out += en.readPositions(reg2, 15, scanned, scannedWriter)
out += en.readPositions(reg3, 15, scanned, scannedWriter)
out += en.readPositions(reg4, 15, scanned, scannedWriter)

duration = time.time() - start_time

print(f"Duration: {duration}")

print(out)

scanned.show()
img.show()