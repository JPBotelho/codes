
from PIL import Image, ImageDraw
from bitstring import Bits, BitArray, BitStream, pack
import encodeUtil as en
import cv2 as cv 
import util

img = Image.open("test.png", mode="r", formats=None)
imgDraw = ImageDraw.Draw(img)


dataString = "Hello World! Hello World! Hello World!"
data = BitArray(bytes(dataString, "utf-8"))

en.encodeData(imgDraw, data, 67, 290, 120, 420, 30)

img.show()
img.save("farto.png")

encoded = cv.imread('farto.png', 0)
# encoded = cv.cvtColor(encoded, cv.COLOR_BGR2GRAY)
cv.imshow("aoieaoi", encoded)
text = en.decodeDataUTF(encoded, 67, 290, 120, 420, 30)
print(text)