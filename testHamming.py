import encodeUtil as en

data = [ 0b00001010, 0b10011001 ]

processed = en.encode(data, 25, 3)

print(processed)
processedBit = en.byteArrayToBitArray(processed)
print(processedBit)

decoded = en.decode(processedBit)

print(decoded)