
from PIL import Image, ImageDraw
import encodeUtil as en

img = Image.open("test.png", mode="r", formats=None)
imgDraw = ImageDraw.Draw(img)

en.encodeData(imgDraw, 67, 290, 120, 420, 20)

img.show()

