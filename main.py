#!/usr/bin/env python3
from random import Random
from typing import List

Loop = str

initial = 0

# TODO how to cache them efficiently?... strings are easiest I guess

def as_loop(*l) -> Loop:
    return ''.join(map(str, l))

Node = int

class Thing:
    def __init__(self, graph):
        self.graph = graph

    @property
    def N(self):
        return len(self.graph)

    @property
    def initial(self):
        return 0

    # def rewrites(self):
    #     rr = {}
    #     for ff, tts in self.graph.items():
    #         for tt in tts:
    #             rr[(as_loop(ff, tt, ff))] = str(ff)
    #     return rr
    # TODO shit, that's sort of dodgy and hacky... how do we know that?
    def rewrites(self):
        rr = {}
        # for ff, tts in self.graph.items():
        #     for tt in tts:
        #         rr[(as_loop(ff, tt, ff))] = str(ff)
        for a in self.graph:
            for b in self.graph:
                for c in self.graph:
                    rr[(as_loop(a, b, c))] = as_loop(a, c) if a != c else str(a) # TODO rename to as_path
                    # TODO don't like it, very hacky!
        return rr

    def walk(self, cur: Node, gen: Random):
        return gen.choice(self.graph[cur])


loop3 = Thing({
    0: (1, 2),
    1: (0, 2),
    2: (0, 1),
})

sphere3 = Thing({
    0: (1, 2, 3),
    1: (0, 2, 3),
    2: (0, 1, 3),
    3: (0, 1, 2),
})

thing = loop3
thing = sphere3



rewrites = thing.rewrites()

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
        l = as_loop(thing.initial)
        while True:
            # TODO just generate all paths of certain complexity??
            cur = int(l[-1])
            if cur == initial and l not in self._contraction:
                return self.contraction(l) # TODO looks a bit meh...
                # if self.g.random() < 0.5: # TODO make configurable
                #     return l
            nn = str(thing.walk(cur, self.g))
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

for _ in range(1000):
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



