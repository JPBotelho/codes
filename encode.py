from PIL import Image, ImageDraw
from math import cos, sin, pi

center = (500, 500)

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

def drawCircle(angle, d, r, col, img):        
    a = toRad(angle)
    dist = d * 1000
    c = toCart(a, dist, center)
    circle(img, c, r, col)

def drawSector(angleStart, angleStop, d, r, col, img):
    angle = angleStart
    step = (r * 2 * 360) / ( 2 * pi * d *1000)
    print(step) 
    while angle < angleStop:
        drawCircle(angle, d, r, col, img)
        angle += step

img = Image.new("RGB", (1000, 1000), color=(255, 255, 255))
img1 = ImageDraw.Draw(img)

r = 125
color = (0, 0, 0)
circle(img1, center, r, color)

#angle = toRad(45)
#crl = 0.2 * 1000

#center = toCart(angle, crl, center)

#circle(img1, center, 25, (255, 0, 0))
drawCircle(angle=45, d=0.4, r=15, col=(255, 0, 255), img=img1)
drawCircle(angle=65, d=0.2, r=15, col=(255, 0, 255), img=img1)
drawSector(90, 180, 0.2, 15, (255, 0, 100), img1)
# drawCircle(45, 0.2, 15, img1, (255, 0, 255))
# drawCircle(45, 0.6, 15, img1, (255, 0, 255))
#img1.ellipse((x-r, y-r, x+r, y+r), fill=(255, 255, 255))
img.show()