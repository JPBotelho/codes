from PIL import Image, ImageDraw

def encodeSector(imgDraw, xpos, ypos, width, height, pixelSize):
    for x in range(xpos, xpos + width, pixelSize):
        for y in range(ypos, ypos + height, pixelSize):
            top_left = (xpos, ypos)
            bottom_right = (xpos + pixelSize, ypos + pixelSize)
            
            imgDraw.rectangle((top_left, bottom_right), fill="black")
    print("finished")
    