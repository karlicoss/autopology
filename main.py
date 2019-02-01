#!/usr/bin/env python3
from random import Random
from typing import List

Loop = str

initial = 0

# TODO how to cache them efficiently?... strings are easiest I guess

class Gen:
    def __init__(self):
        self.g = Random(1234)
        self._cache = set()


    def cache(self, l: Loop):
        # ss = ''join(map(str, l))
        self._cache.add(l)

    def cached(self, l: Loop):
        # ss = ''.join(map(str, l))
        return l in self._cache

    def gen(self) -> Loop:
        l = '0'
        while True:
            # TODO just generate all paths of certain complexity??
            cur = int(l[-1])
            if cur == initial:
                if not self.cached(l):
                    self.cache(l)
                    return l
                # if self.g.random() < 0.5: # TODO make configurable
                #     return l
            nn = str((cur + self.g.choice([-1, 1])) % 3)
            l += nn

N = 3

def as_loop(*l) -> Loop:
    return ''.join(map(str, l))

rewrites = {}
for b in range(N):
    for delta in (-1, 1):
        rewrites[as_loop(b, (b + delta) % N, b)] = str(b)
# for ff, tt in rewrites.items():
#     print(f'{ff} -> {tt}')

class Contractor:
    def __init__(self):
        self.g = Random(1234)
        self.m = {'0': '0'}

    def contract(self, l: Loop, maxsteps=1000) -> Loop:
        # TODO check if exists
        # rr = self.m.get(l, None)
        # if rr is not None:
        #     return rr

        for s in range(maxsteps):
            for ff, tt in rewrites.items():
                # TODO shit we can't contract any of the 
                l = l.replace(ff, tt)
        return l

g = Gen()

loops = [g.gen() for _ in range(1000)]

cc = Contractor()
cmap = {}
for l in loops:
    ctd = cc.contract(l)
    cmap[l] = ctd
    print(l + " -> " + ctd)

print("Contracted elements:")

for res in sorted(set(cmap.values())):
    print(res)


