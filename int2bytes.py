# int to bytes test

i = 1024
b = (i).to_bytes(2, byteorder='big')

#speedArr = list(bytearray((speed).to_bytes(4, byteorder='little', signed=True)))



# int from bytes test

rpl = [0x01, 0xe8, 0xfd, 0x00, 0x00, 0x07]
print(rpl)
print(rpl[1:5])

rplInt = int.from_bytes(bytes(bytearray(rpl[1:5])), byteorder='little', signed=True)
print(rplInt)
