import encodeUtil as en

minDist = 325
maxDist = 465
amplitude = 65

points = en.getPointsInRegion(amplitude, 90, minDist, maxDist, 27)

print(len(points))