
# LIST FLATTENING TOOL
from collections.abc import Iterable                            
def flatFunc(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatFunc(x)
        else:
            yield x

def flatList(inpArr1):
    return list(flatFunc(inpArr1))



flat = flatList([1,['abc',3],'xyz'])
print(flat)