

import collections
def flatList(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatList(i)]
    else:
        return [x]

def xor(arr, mode):
    if mode == "reqMode":
        idxList = [i for i, val in enumerate(arr) if val == 0x7d]

        for idx in idxList:
            arr[idx] = [0x7d, arr[idx]^0x20]
            
        arr  = flatList(arr) 

        idxList = [i for i, val in enumerate(arr) if val == 0x7e]
        idxList.pop(-1)
        idxList.pop(0)

        for idx in idxList:
            arr[idx] = [0x7d, arr[idx]^0x20]
            
        arrXOR = flatList(arr) 
        return(arrXOR)

    if mode == "rplMode":
        idxList = [i for i, val in enumerate(arr) if val == 0x7d]

        for idx in idxList:
            arr[idx+1] = arr[idx+1]^0x20

        idxList.reverse()
        for idx in idxList:
            arr.pop(idx)

        arrTrue = arr
        return(arrTrue)





reqArr = [126, 3, 126, 125, 126, 0, 126]
print(xor(reqArr,"reqMode"))

rplArr = [126, 3, 125, 94, 125, 93, 125, 94, 0, 126]
print(xor(rplArr,"rplMode"))





