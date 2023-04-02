import encodeUtil as en
data = []
length = 40
id = 3
infoByte = bin((length << 2) + id)
data.insert(0, int(infoByte, 2))
data.append(infoByte)
print(data)