SIZE = 1000
CENTER = (SIZE // 2, SIZE // 2)

from math import cos, sin, pi

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
    dist = d
    c = toCart(a, dist, CENTER)
    circle(img, c, r, col)
