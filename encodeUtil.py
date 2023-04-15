from PIL import Image, ImageDraw
import cv2 as cv

def encodeData(imgDraw, data, xpos, ypos, width, height, pixelSize):
    index = 0
    for x in range(xpos, xpos + width, pixelSize):
        for y in range(ypos, ypos + height, pixelSize):
            top_left = (x, y)
            bottom_right = (x + pixelSize, y + pixelSize)
            
            color = "black"
            
            if index < len(data):
                val = data[index]
                if val:
                    color = "white"
            index+=1
                            
            imgDraw.rectangle((top_left, bottom_right), fill=color)
    print("finished")
    
def readPos(img, xpos, ypos, pixelSize, thres):
    accum = 0
    iter = 0
    pixelSize = pixelSize // 2
    for x in range(xpos, xpos + pixelSize):
        for y in range(ypos, ypos + pixelSize):
            accum += img[y][x]
            iter += 1
    
    return (accum / iter) > thres

def circle(img, center, r, color):
    x = center[0]
    y = center[1]
    cv.circle(img, center, r, color, 2)
    
def decodeDataUTF(og, img, xpos, ypos, width, height, pixelSize):
    currentByte = []
    output = ""
    for x in range(xpos, xpos + width, pixelSize):
        for y in range(ypos, ypos + height, pixelSize):            
            boolVal = readPos(img, x, y, pixelSize, 128)
            center = (x + pixelSize // 2, y + pixelSize // 2)
            if boolVal:
                currentByte.append(1)
                cv.circle(og, center, pixelSize//2, (255, 0, 0))
            else:
                currentByte.append(0)
                cv.circle(og, center, pixelSize//2, (0, 0, 255))
            if len(currentByte) == 8:
                byteStr = "".join(str(b) for b in currentByte[::])
                intVal = int(byteStr, 2)
                c = chr(intVal)
                output += c
                currentByte = []
    return output
    
def drawPos(img, xpos, ypos, width, height, pixelSize):
    for x in range(xpos, xpos + width, pixelSize):
        for y in range(ypos, ypos + height, pixelSize):
            center = (x + pixelSize // 2, y + pixelSize // 2)
            cv.circle(img, center, pixelSize//2, (25, 0, 0))