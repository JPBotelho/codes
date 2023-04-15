from PIL import Image, ImageDraw

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
    for x in range(xpos, xpos + pixelSize):
        for y in range(ypos, ypos + pixelSize):
            accum += img[x][y]
            iter += 1
    
    return (accum / iter) > thres

def decodeDataUTF(img, xpos, ypos, width, height, pixelSize):
    currentByte = []
    output = ""
    for x in range(xpos, xpos + width, pixelSize):
        for y in range(ypos, ypos + height, pixelSize):            
            boolVal = readPos(img, x, y, pixelSize, 128)
            if boolVal:
                currentByte.append(1)
            else:
                currentByte.append(0)
            if len(currentByte) == 8:
                byteStr = "".join(str(b) for b in currentByte[::])
                intVal = int(byteStr, 2)
                c = chr(intVal)
                output += c
                currentByte = []
    return output
    