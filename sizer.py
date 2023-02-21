from datetime import datetime
from sys import getsizeof as sys_getsizeof
from types import ModuleType, FunctionType
from gc import get_referents

from flashcard import Flashcard

def getsize(obj):
    """sum size of object & members."""
    BLACKLIST = type, ModuleType, FunctionType
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys_getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size


def getdictsize(d):
    return sum([getsize(k) + getsize(d[k]) for k in d])

gib_to_bytes = lambda gib: gib * 1073741824

bytes_to_gib = lambda bytes: bytes / 1073741824



a = {str(k): Flashcard('ad' * (500 + k), 'bru' * (500 + k), datetime(2023, 4, 11, 12, 1, 4)) for k in range(10)}
b = {str(k): Flashcard('ad' * (500 + k), 'bru' * (500 + k), datetime(2023, 4, 11, 12, 1, 4)) for k in range(10)}

print(getsize(Flashcard('ad' * 500, 'bru' * 500, datetime(2023, 4, 11, 12, 1, 4))))

total_instances_a = 512 / bytes_to_gib(getdictsize(a) / 10)
total_instances_b = 512 / bytes_to_gib(getdictsize(b) / 10)

print(total_instances_a / 2_500)
print(total_instances_b / 2_500)



t1 = """els = (-1, )
for i in range(30):
    els += (i, )
"""

t2 = """els = [-1]
for i in range(30):
    els.append(i)
"""

t3 = """import numpy as np
els = np.array([-1])
for i in range(30):
    els = np.append(els, i)
"""

from timeit import timeit

print('Tupla:', timeit(
    stmt=t1,
    number=10_000_000
))
print('Lista:', timeit(
    stmt=t2,
    number=10_000_000
))
print('Array de Numpy:', timeit(
    stmt=t3,
    number=10_000_000
))