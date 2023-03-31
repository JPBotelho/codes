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
        en.drawSector(angleStart, angleStop, slice, n, color, img, True)
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
en.readRegion(70, 90, minDist, maxDist, 15, (255, 0, 0), img)

drawRegion(70, 0, minDist, maxDist, 15, (255, 0, 0), img1)
en.readRegion(70, 0, minDist, maxDist, 15, (255, 0, 0), img)

drawRegion(70, 180, minDist, maxDist, 15, (255, 0, 0), img1)
en.readRegion(70, 180, minDist, maxDist, 15, (255, 0, 0), img)

drawRegion(70, 270, minDist, maxDist, 15, (255, 0, 0), img1)
en.readRegion(70, 270, minDist, maxDist, 15, (255, 0, 0), img)


    
shapeUp = [(500, 500), (500, 0)]
shapeLeft = [(500, 500), (0, 500)]

print(f"Drew {accum} circles")

# im = np.asarray(img)

print(img.getpixel((222, 222)))
img.show()