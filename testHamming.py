import encodeUtil as en

data = [ 10, 153 ]

processed = en.encode(data, 16, 1)
processedBit = en.byteArrayToBitArray(processed)
decoded = en.decode(processedBit)

sectorId = decoded[0]
dataLength = decoded[1]
readData = decoded[2]

print(f"Sector: {sectorId}")
print(f"Length: {dataLength}")
print(f"Data: {readData}")