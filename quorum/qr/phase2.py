"""Phase 2: voter census.  Forward move after each voter's events, alone, aligned with the Smart Trend regime,
and for every pair of different techniques that agrees within the window.  Discover folds, replicated on Confirm."""
import json
import sys

import numpy as np
from scipy import stats as st

from .common import SYMS, bars, atr14, split_mask, RT_USD
from . import lc, voters
from .consensus import quorum

H = 6          # primary horizon in bars
W = 2          # the owner's default window
TF = int(sys.argv[1]) if len(sys.argv) > 1 else 5


def fwd(b, a):
    """Per-bar forward signed-unit move for a long entered at the next open and held H bars (or to the close)."""
    idx = np.arange(b.n)
    ok = ~b.last & ~np.isnan(a)
    j = np.minimum(idx + 1 + H, b.n - 1)
    end = b.sess_end
    px = np.where(idx + 1 + H <= end, b.o[j], b.c[end])
    ent = b.o[np.minimum(idx + 1, b.n - 1)]
    r = (px - ent) / a
    cost = RT_USD[b.sym] / b.pv / a
    return np.where(ok, r, np.nan), np.where(ok, cost, np.nan)


ctx = {}
for sym in SYMS:
    b = bars(sym, TF)
    a = atr14(b)
    names, fams, EV, ids, params = voters.build(sym, TF)
    r, cost = fwd(b, a)
    _, reg, _, _ = lc.smart_arrows(b)
    ctx[sym] = dict(b=b, EV=EV, r=r, cost=cost, reg=reg, disc=split_mask(b, "discover"), conf=split_mask(b, "confirm"))
V = len(names)
NS = {k: sum(len(np.unique(ctx[s]["b"].sess[ctx[s][k]])) for s in SYMS) / 2 for k in ("disc", "conf")}


def summarize(sig_by_sym):
    """sig_by_sym: {sym: int8 array of +1/-1/0}.  Returns stats for discover and confirm (net of costs, ATR units)."""
    out = {}
    for blk in ("disc", "conf"):
        rs, ss = [], []
        for sym in SYMS:
            c = ctx[sym]
            s = sig_by_sym[sym]
            m = (s != 0) & c[blk] & ~np.isnan(c["r"])
            rs.append(s[m] * c["r"][m] - c["cost"][m])
            ss.append(c["b"].sess[m])
        r = np.concatenate(rs)
        sess = np.concatenate(ss)
        n = len(r)
        if n < 30:
            out[blk] = dict(n=n, per_day=n / NS[blk] / 2, mean=np.nan, t=np.nan, win=np.nan)
            continue
        u, inv = np.unique(sess, return_inverse=True)
        ssum, cnt = np.bincount(inv, r), np.bincount(inv)
        mean = r.mean()
        se = np.sqrt(((ssum - cnt * mean) ** 2).sum()) / n
        out[blk] = dict(n=n, per_day=n / NS[blk] / 2, mean=float(mean), t=float(mean / se), win=float((r > 0).mean() * 100))
    return out


res = {"alone": {}, "with_regime": {}, "against_regime": {}, "pairs": {}}
for v in range(V):
    res["alone"][names[v]] = summarize({s: ctx[s]["EV"][v] for s in SYMS})
    res["with_regime"][names[v]] = summarize({s: np.where(ctx[s]["EV"][v] == ctx[s]["reg"], ctx[s]["EV"][v], 0).astype(np.int8) for s in SYMS})
    res["against_regime"][names[v]] = summarize({s: np.where(ctx[s]["EV"][v] == -ctx[s]["reg"], ctx[s]["EV"][v], 0).astype(np.int8) for s in SYMS})
z = np.zeros(1, np.bool_)
for i in range(V):
    for j in range(i + 1, V):
        if ids[i] == ids[j]:
            continue
        sig = {}
        for s in SYMS:
            L, Sx = quorum(ctx[s]["EV"], np.array([i, j]), W, 2, False, z, z)
            sig[s] = L.astype(np.int8) - Sx.astype(np.int8)
        res["pairs"][f"{names[i]} + {names[j]}"] = summarize(sig)
    if i % 20 == 0:
        print("pairs", i, flush=True)
json.dump(res, open(f"reports/phase2_tf{TF}.json", "w"), default=float)


def show(title, d, top=15, min_day=0.2):
    rows = [(k, v) for k, v in d.items() if v["disc"]["n"] >= 30 and v["disc"]["per_day"] >= min_day and not np.isnan(v["disc"]["t"])]
    rows.sort(key=lambda kv: -kv[1]["disc"]["t"])
    print(f"\n{title}: {len(rows)} tested; top {top} by Discover t   (net move after costs, ATR units, {H} bars)")
    print(f"{'name':58s} {'ev/day':>6s} | disc mean  t   win% | conf mean  t   win%")
    for k, v in rows[:top]:
        d_, c_ = v["disc"], v["conf"]
        print(f"{k[:58]:58s} {d_['per_day']:6.2f} | {d_['mean']:+.3f} {d_['t']:+5.1f} {d_['win']:4.0f} | {c_['mean']:+.3f} {c_['t']:+5.1f} {c_['win']:4.0f}")
    t_d = np.array([v["disc"]["t"] for k, v in rows])
    t_c = np.array([v["conf"]["t"] for k, v in rows])
    m_d = np.array([v["disc"]["mean"] for k, v in rows])
    m_c = np.array([v["conf"]["mean"] for k, v in rows])
    ok = ~np.isnan(t_c)
    p = 1 - st.norm.cdf(t_d)
    order = np.argsort(p)
    bh = np.zeros(len(p), bool)
    thr = 0.10 * (np.arange(len(p)) + 1) / len(p)
    passed = np.flatnonzero(p[order] <= thr)
    if len(passed):
        bh[order[:passed.max() + 1]] = True
    print(f"  share with positive net move: discover {100 * (m_d > 0).mean():.0f}%, confirm {100 * (m_c[ok] > 0).mean():.0f}%")
    print(f"  discover t > 2: {(t_d > 2).sum()}; of those, confirm mean > 0: {(m_c[(t_d > 2) & ok] > 0).sum()}, confirm t > 2: {(t_c[(t_d > 2) & ok] > 2).sum()}")
    print(f"  pass Benjamini-Hochberg at 10% on discover: {bh.sum()}; of those confirm mean > 0: {(m_c[bh & ok] > 0).sum()}, confirm t > 2: {(t_c[bh & ok] > 2).sum()}")
    print(f"  rank correlation of discover t with confirm t: {st.spearmanr(t_d[ok], t_c[ok])[0]:+.2f}")
    if (bh & ok).any():
        print(f"  BH survivors: discover mean {m_d[bh & ok].mean():+.3f} -> confirm mean {m_c[bh & ok].mean():+.3f}")


show("Voters alone", res["alone"])
show("Voter events in the direction of the Smart Trend regime", res["with_regime"])
show("Voter events against the Smart Trend regime", res["against_regime"])
show("Pairs of different techniques agreeing within 2 bars", res["pairs"], top=25)
