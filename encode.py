from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
import numpy as np 
import random as rnd
import time 

DATA_STRING = "HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD! HELLO, WORLD!"
WRITE_BITS = []

WRITE_BITS = en.strToBitArray(DATA_STRING, 50)
ENCODED_STRING = en.bitArrayToString(WRITE_BITS)

img = Image.open("test.png", mode="r", formats=None)
imgDraw = ImageDraw.Draw(img)

minDist = 325
maxDist = 465
amplitude = 65

reg1 = en.getPointsInRegion(amplitude, 90, minDist, maxDist, 35)
reg2 = en.getPointsInRegion(amplitude, 0, minDist, maxDist, 35)
reg3 = en.getPointsInRegion(amplitude, 180, minDist, maxDist, 35)
reg4 = en.getPointsInRegion(amplitude, 270, minDist, maxDist, 35)
print(len(reg1))
en.encodePoints(reg1, WRITE_BITS, 35, imgDraw)
en.encodePoints(reg2, WRITE_BITS, 35, imgDraw)
en.encodePoints(reg3, WRITE_BITS, 35, imgDraw)
en.encodePoints(reg4, WRITE_BITS, 35, imgDraw)

scanned = Image.open("out.png", mode="r", formats=None)
scanned = scanned.convert('L')
#scanned = scanned.point( lambda p: 255 if p > 200 else 0 )

scannedWriter = ImageDraw.Draw(scanned)
readSectors = []
secondarySectors = []
thirdSectors = []
sectors = []
readRes = en.readPositions(reg1, 15, scanned, False, scannedWriter)
readSectors.append(readRes[0])
secondarySectors.append(readRes[1])
thirdSectors.append(readRes[2])

readRes = en.readPositions(reg2, 15, scanned, False, scannedWriter)
readSectors.append(readRes[0])
secondarySectors.append(readRes[1])
thirdSectors.append(readRes[2])

readRes = en.readPositions(reg3, 15, scanned, False, scannedWriter)
readSectors.append(readRes[0])
secondarySectors.append(readRes[1])
thirdSectors.append(readRes[2])

readRes = en.readPositions(reg4, 15, scanned, False, scannedWriter)
readSectors.append(readRes[0])
secondarySectors.append(readRes[1])
thirdSectors.append(readRes[2])

for i in range(len(readSectors)):
    readString = en.bitArrayToString(readSectors[i])
    validity = en.checkValidity(ENCODED_STRING, readString)

    secondString = en.bitArrayToString(secondarySectors[i])
    secondValidity = en.checkValidity(ENCODED_STRING, secondString)
    
    thirdString = en.bitArrayToString(thirdSectors[i])
    thirdValidity = en.checkValidity(ENCODED_STRING, thirdString)
    
    print(f"Sector {i}: {max(validity, secondValidity, thirdValidity)}")

scanned.show()
img.show()