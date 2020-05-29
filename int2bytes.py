# int to bytes test

i = 1024
b = (i).to_bytes(2, byteorder='big')

print(i)
print(b)
print(int(b))