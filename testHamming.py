import encodeUtil as en

data = [0, 1, 0, 1]
encodedBlock = en.encodeBlock(data)
encodedBlock[3] = 1
encodedBlock[4] = 1
decodedData = en.decodeBlock(encodedBlock)

print(decodedData)