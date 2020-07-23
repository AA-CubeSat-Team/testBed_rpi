
# LIST FLATTENING TOOL
import collections
def flatList(inpArr1):
    if isinstance(inpArr1, collections.Iterable):
        return [a for i in inpArr1 for a in flatList(i)]
    else:
        return [inpArr1]


print(flatList([1, ['abc', 4], 5]))