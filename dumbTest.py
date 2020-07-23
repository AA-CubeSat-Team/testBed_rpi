
# LIST FLATTENING TOOL
import collections.abc
def flatList1(inpArr1):
    if isinstance(inpArr1, collections.abc.Iterable):
        return [a for i in inpArr1 for a in flatList1(i)]
    else:
        return [inpArr1]

def flatList2(inpArr1):
    newlist = [j for i in inpArr1 for j in i]
    return newlist

from collections import Iterable                            # < py38
def flatList3(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatList3(x)
        else:
            yield x


flat = sum([[1], ['abc', 4], [5]],[])

flat = flatList3([1, ['abc', 4], 5])


print(list(flat))