#!/usr/bin/env python3
from random import Random
from typing import List

Loop = str

initial = 0

# TODO how to cache them efficiently?... strings are easiest I guess

def as_loop(*l) -> Loop:
    return ''.join(map(str, l))

N = 3
rewrites = {}
for b in range(N):
    for delta in (-1, 1):
        rewrites[as_loop(b, (b + delta) % N, b)] = str(b)

class Gen:
    def __init__(self):
        self.g = Random(1234)
        self._contraction = {}


    # def cache(self, l: Loop):
    #     # ss = ''join(map(str, l))
    #     self._cache.add(l)

    # def cached(self, l: Loop):
    #     # ss = ''.join(map(str, l))
    #     return l in self._cache

    def gen(self) -> Loop:
        l = '0'
        while True:
            # TODO just generate all paths of certain complexity??
            cur = int(l[-1])
            if cur == initial and l not in self._contraction:
                return self.contraction(l) # TODO looks a bit meh...
                # if self.g.random() < 0.5: # TODO make configurable
                #     return l
            nn = str((cur + self.g.choice([-1, 1])) % N)
            l += nn

    def contraction(self, l: Loop, maxsteps=1000) -> Loop:
        cseq = [l] # sequence leading to trivial loop

        def alala(target: Loop):
            for c in cseq:
                # assert c not in self._contraction
                self._contraction[c] = target

        for s in range(maxsteps):
            last = cseq[-1]
            cc = self._contraction.get(last, None)
            if cc is not None:
                alala(cc)
                return cc
            else:
                for ff, tt in rewrites.items():
                    nl = last.replace(ff, tt)
                    if len(nl) < len(last):
                        # ok, something changed, give it another chance..
                        cseq.append(nl)
                        break
                else:
                    alala(last)
                    return last
        raise RuntimeError # TODO ???? just mark as trivial?

# for ff, tt in rewrites.items():
#     print(f'{ff} -> {tt}')

g = Gen()

for _ in range(100000):
    print(g.gen())
print("Contracted elements:")

for res in sorted(set(g._contraction.values())):
    print(res)

# loops = [g.gen() for _ in range(3000)]

# cc = Contractor()
# cmap = {}
# for l in loops:
#     ctd = cc.contract(l)
#     cmap[l] = ctd
#     print(l + " -> " + ctd)



