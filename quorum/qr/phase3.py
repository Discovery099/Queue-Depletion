"""Phase 3: quorum search on the Discover folds only.  4 islands x 25,000 evaluations = 100,000."""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

from . import search as Q
from .common import ROOT

N_PER = int(sys.argv[1]) if len(sys.argv) > 1 else 25000
SEED = 20261115


def niche(g, s):
    return (g["mode"], g["exit"][0], min(int(s["tpd"]), 6), len(g["panel"]))


def island(i):
    rng = np.random.default_rng(SEED + i)
    e = Q.env(5)
    V, ids = len(e["names"]), e["ids"]
    seen, elites, top = {}, {}, []
    log = open(os.path.join(ROOT, "cache", f"phase3_island{i}.jsonl"), "w")
    t0 = time.time()
    for it in range(N_PER):
        if it < 2500 or not elites:
            g = Q.rand_genome(rng, V, ids)
        else:
            pool = [x[1] for x in top] if rng.random() < 0.5 else [v[1] for v in elites.values()]
            par = pool[int(rng.integers(len(pool)))]
            oth = pool[int(rng.integers(len(pool)))]
            g = Q.mutate(par, rng, V, ids, oth)
        k = Q.gkey(g)
        if k in seen:
            g = Q.rand_genome(rng, V, ids)
            k = Q.gkey(g)
            if k in seen:
                continue
        fit, s = Q.fitness(g, e)
        seen[k] = fit
        log.write(json.dumps(dict(it=it, fit=fit, g=g, s=s)) + "\n")
        nk = niche(g, s)
        if nk not in elites or fit > elites[nk][0]:
            elites[nk] = (fit, g)
        if len(top) < 50 or fit > top[-1][0]:
            top.append((fit, g))
            top.sort(key=lambda x: -x[0])
            top = top[:50]
        if it % 2500 == 0:
            print(f"island {i} it {it} {time.time() - t0:.0f}s best {top[0][0]:.3f} niches {len(elites)}", flush=True)
    log.close()
    return i


if __name__ == "__main__":
    Q.env(5)                      # warm caches and numba before forking
    with Pool(4) as p:
        p.map(island, range(4))
    print("done")
