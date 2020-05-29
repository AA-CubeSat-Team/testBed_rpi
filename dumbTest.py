data1 = [101, 201]
print(type(data1))

data1x = hex(data1)
row1_ll = [[kk], [time1], data1x]
row1  = [val for sublist in row1_ll for val in sublist]
print(row1)