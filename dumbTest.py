
# LIST FLATTENING TOOL
import collections
def flatList1(inpArr1):
    if isinstance(inpArr1, collections.Iterable):
        return [a for i in inpArr1 for a in flatList(i)]
    else:
        return [inpArr1]

def flatList2(inpArr1):
    newlist = [j for i in inpArr1 for j in i]
    return newlist


print(flatList([1, ['abc', 4], 5]))