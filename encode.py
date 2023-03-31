from PIL import Image, ImageDraw
from math import cos, sin, pi
import encodeUtil as en
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
        en.drawSector(angleStart, angleStop, slice, n, color, img)
        accum += n



#img = Image.new("RGB", (1000, 1000), color=(255, 255, 255))
img = Image.open("test.png", mode="r", formats=None)
img1 = ImageDraw.Draw(img)

r = 125
color = (0, 0, 0)
# drawSector(0, 360, 270, 90*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 285, 96*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 300, 102*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 315, 108*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 330, 114*1.5, (255, 0, 100), img1)
# drawSector(0, 360, 345, 120*1.5, (255, 0, 100), img1)

minDist = 325
maxDist = 465

drawRegion(70, 90, minDist, maxDist, 15, (255, 0, 0), img1)
drawRegion(70, 0, minDist, maxDist, 15, (255, 0, 0), img1)
drawRegion(70, 180, minDist, maxDist, 15, (255, 0, 0), img1)
drawRegion(70, 270, minDist, maxDist, 15, (255, 0, 0), img1)
# drawRegion(150, 212, minDist, maxDist, 15, (255, 0, 0), img1)
# drawRegion(330, 392, minDist, maxDist, 15, (255, 0, 0), img1)
#drawRegion(240, 302, minDist, maxDist, 15, (255, 0, 0), img1)

    
shapeUp = [(500, 500), (500, 0)]
shapeLeft = [(500, 500), (0, 500)]
#img1.line(shapeUp, fill="red", width = 0)
#img1.line(shapeLeft, fill="red", width = 0)
print(f"Drew {accum} circles")
# drawCircle(45, 0.2, 15, img1, (255, 0, 255))
# drawCircle(45, 0.6, 15, img1, (255, 0, 255))
#img1.ellipse((x-r, y-r, x+r, y+r), fill=(255, 255, 255))
img.show()