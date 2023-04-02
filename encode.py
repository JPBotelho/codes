
from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
import numpy as np 
import random as rnd
import time 

text = "TESTE"
bitArr = en.strToBitArray(text, 40)
byteArr = en.bitArrayToByteArray(bitArr)
encodedData1 = en.byteArrayToBitArray(en.encode(byteArr, 40, 1))
encodedData2 = en.byteArrayToBitArray(en.encode(byteArr, 40, 2))
encodedData3 = en.byteArrayToBitArray(en.encode(byteArr, 40, 3))
encodedData4 = en.byteArrayToBitArray(en.encode(byteArr, 40, 4))

img = Image.open("test.png", mode="r", formats=None)
imgDraw = ImageDraw.Draw(img)

minDist = 325
maxDist = 465
amplitude = 65

reg1 = en.getPointsInRegion(amplitude, 90, minDist, maxDist, 30)
reg2 = en.getPointsInRegion(amplitude, 0, minDist, maxDist, 30)
reg3 = en.getPointsInRegion(amplitude, 180, minDist, maxDist, 30)
reg4 = en.getPointsInRegion(amplitude, 270, minDist, maxDist, 30)
#print(len(reg1))
en.encodePoints(reg1, encodedData1, 30, imgDraw)
en.encodePoints(reg2, encodedData2, 30, imgDraw)
en.encodePoints(reg3, encodedData3, 30, imgDraw)
en.encodePoints(reg4, encodedData4, 30, imgDraw)

img.show()