"""Literal bar-by-bar Python port of the regular-hours engine in pine/SmartTrend_Enhanced.pine
(sections 2 and 6). Used by tests/test_pine_parity.py to check it matches the research engine."""
import math
import numpy as np

NA = float("nan")
na = lambda x: x is None or (isinstance(x, float) and math.isnan(x))


class SmartState:
    def __init__(self):
        self.trail = NA; self.regime = 0; self.prevRegime = 0; self.prevClose = NA
        self.trSum = 0.0; self.trCnt = 0; self.rawAtr = NA; self.atr = NA; self.flipBuy = False; self.flipSell = False

    def update(s, c, h, l, ln, smooth, sLen, factor):
        tr = h - l if na(s.prevClose) else max(h - l, abs(h - s.prevClose), abs(l - s.prevClose))
        if na(s.rawAtr):
            s.trSum += tr; s.trCnt += 1
            if s.trCnt >= ln:
                s.rawAtr = s.trSum / ln
        else:
            s.rawAtr = (tr + (ln - 1) * s.rawAtr) / ln
        if not na(s.rawAtr):
            al = 2.0 / (sLen + 1)
            s.atr = s.rawAtr if not smooth else (s.rawAtr if na(s.atr) else al * s.rawAtr + (1 - al) * s.atr)
        buf = NA if na(s.atr) else factor * s.atr
        if na(s.trail) and not na(buf):
            s.trail = c
            s.regime = 1 if (not na(s.prevClose) and c > s.prevClose) else -1
        if not na(s.trail) and not na(buf):
            raw = max(s.trail, c - buf) if s.regime == 1 else min(s.trail, c + buf)
            nx = -1 if (s.regime == 1 and c < raw) else (1 if (s.regime == -1 and c > raw) else s.regime)
            if nx != s.regime:
                s.regime = nx; s.trail = c - buf if s.regime == 1 else c + buf
            else:
                s.trail = raw
        s.flipBuy = s.regime == 1 and s.prevRegime == -1
        s.flipSell = s.regime == -1 and s.prevRegime == 1
        s.prevRegime = s.regime; s.prevClose = c
        return s.regime


class HtfAgg:
    def __init__(self):
        self.curKey = -1; self.h = NA; self.l = NA; self.c = NA; self.st = SmartState()

    def push(g, key, h, l, c, ln, sLen, factor):
        if key != g.curKey:
            if g.curKey != -1:
                g.st.update(g.c, g.h, g.l, ln, True, sLen, factor)
            g.curKey = key; g.h = h; g.l = l
        else:
            g.h = max(g.h, h); g.l = min(g.l, l)
        g.c = c
        return g.st.regime


class Rma:
    def __init__(self):
        self.sum = 0.0; self.cnt = 0; self.val = NA

    def step(r, x, n):
        if not na(x):
            if na(r.val):
                r.sum += x; r.cnt += 1
                if r.cnt >= n:
                    r.val = r.sum / n
            else:
                r.val = (x + (n - 1) * r.val) / n
        return r.val


def f_push(buf, x, cap):
    buf.append(x)
    if len(buf) > cap:
        buf.pop(0)


def f_wma(buf, n):
    sz = len(buf)
    if n >= 1 and sz >= n:
        return sum(buf[sz - 1 - k] * (n - k) for k in range(n)) / (n * (n + 1) / 2.0)
    return NA


class Hma:
    def __init__(self, ln):
        self.len = ln; self.raw = []; self.val = NA; self.prev = NA

    def step(m, closes):
        half = max(1, int(m.len / 2)); sq = max(1, int(math.floor(math.sqrt(m.len))))
        w1 = f_wma(closes, half); w2 = f_wma(closes, m.len)
        m.prev = m.val
        if not na(w1) and not na(w2):
            f_push(m.raw, 2 * w1 - w2, 64)
        m.val = f_wma(m.raw, sq)
        return m.val


def f_er(buf, n):
    sz = len(buf)
    if sz >= n + 1:
        den = sum(abs(buf[sz - 1 - k] - buf[sz - 2 - k]) for k in range(n))
        return abs(buf[-1] - buf[sz - 1 - n]) / den if den > 0 else 0.0
    return NA


def f_diff(buf, n):
    sz = len(buf)
    return buf[-1] - buf[sz - 1 - n] if sz >= n + 1 else NA


def f_rsi(up, dn):
    if na(up) or na(dn):
        return NA
    return 100.0 if dn == 0 else (0.0 if up == 0 else 100.0 - 100.0 / (1.0 + up / dn))


def run(b, roll, atrLength=14, smoothAtr=True, smoothLength=10, trailFactor=2.0, useRecovery=True,
        hmaLength=2, rsiF=25, rsiS=100, maxGap=4):
    """b: research Bars (regular-session only). Returns dict of arrays (signals + 24 features per bar)."""
    n = b.n
    out = {k: np.full(n, np.nan) for k in ["atr", "trail", "regime", "htf15", "htf60", "fast", "slow", "adx", "dip", "dim",
                                            "er10", "er20", "er40", "hslope", "ret6", "ret24", "vwap", "atrbase", "volbase",
                                            "barOfDay", "gap", "daypos", "fromopen", "prevday"]}
    mb = np.zeros(n, bool); ms = np.zeros(n, bool)
    st5 = SmartState(); a15 = HtfAgg(); a60 = HtfAgg(); hS = Hma(hmaLength); h21 = Hma(21)
    upF, dnF, upS, dnS, trR, pdmR, mdmR, adxR = (Rma() for _ in range(8))
    cBuf, atrBuf, volBuf = [], [], []
    rtB = 0; dayKey = 0; pC = pH = pL = pFast = pSlow = NA; pRU = pRD = False; shadow = 0
    barOfDay = 0; dayOpen = runHi = runLo = lastC = prevC = prevPrevC = NA; cumPV = cumV = 0.0
    rArm = 0; rBar = None; rTime = None
    sp = hp = rp = 0; sb = hb = rb = None
    for i in range(n):
        o, h, l, c, v = b.o[i], b.h[i], b.l[i], b.c[i], b.v[i]
        if b.first_bar[i]:
            dayKey += 1; barOfDay = 0; dayOpen = o; runHi = h; runLo = l; prevPrevC = prevC; prevC = lastC; cumPV = cumV = 0.0
        else:
            barOfDay += 1; runHi = max(runHi, h); runLo = min(runLo, l)
        cumPV += (h + l + c) / 3 * v; cumV += v; lastC = c; rtB += 1
        st5.update(c, h, l, atrLength, smoothAtr, smoothLength, trailFactor)
        htf15 = a15.push(dayKey * 1000 + int(barOfDay / 3), h, l, c, atrLength, smoothLength, trailFactor)
        htf60 = a60.push(dayKey * 1000 + int(barOfDay / 12), h, l, c, atrLength, smoothLength, trailFactor)
        f_push(cBuf, c, 500)
        if not na(st5.rawAtr):
            f_push(atrBuf, st5.rawAtr, 390)
        f_push(volBuf, v, 390)
        atrBase = sum(atrBuf) / len(atrBuf) if len(atrBuf) >= 390 else NA
        volBase = sum(volBuf) / len(volBuf) if len(volBuf) >= 50 else NA
        chg = NA if na(pC) else c - pC
        fast = f_rsi(upF.step(NA if na(chg) else max(chg, 0.0), rsiF), dnF.step(NA if na(chg) else max(-chg, 0.0), rsiF))
        slow = f_rsi(upS.step(NA if na(chg) else max(chg, 0.0), rsiS), dnS.step(NA if na(chg) else max(-chg, 0.0), rsiS))
        ok = not (na(fast) or na(slow) or na(pFast) or na(pSlow))
        cu = ok and fast > slow and pFast <= pSlow; cd = ok and fast < slow and pFast >= pSlow
        rsiBuy, rsiSell = pRU, pRD; pRU, pRD = cu, cd
        hv = hS.step(cBuf); hmaBuy = hmaSell = False
        if not na(hv) and not na(hS.prev) and not na(pC):
            up_ = c > hv and pC <= hS.prev; dn_ = c < hv and pC >= hS.prev
            if up_ and shadow != 1:
                hmaBuy = True; shadow = 1
            elif dn_ and shadow != -1:
                hmaSell = True; shadow = -1
        hv21 = h21.step(cBuf); hslope = NA if (na(hv21) or na(h21.prev)) else hv21 - h21.prev
        upM = NA if na(pH) else h - pH; dnM = NA if na(pL) else pL - l
        pdm = NA if na(upM) else (upM if (upM > dnM and upM > 0) else 0.0)
        mdm = NA if na(dnM) else (dnM if (dnM > upM and dnM > 0) else 0.0)
        trA = NA if na(pC) else max(h - l, abs(h - pC), abs(l - pC))
        trV = trR.step(trA, 14); pdmV = pdmR.step(pdm, 14); mdmV = mdmR.step(mdm, 14)
        dip = NA if (na(trV) or na(pdmV)) else 100 * pdmV / trV
        dim = NA if (na(trV) or na(mdmV)) else 100 * mdmV / trV
        dx = NA if (na(dip) or na(dim)) else 100 * abs(dip - dim) / max(dip + dim, 1e-12)
        adx = adxR.step(dx, 14)
        reg, a, tr5 = st5.regime, st5.atr, st5.trail
        recB = recS = False
        if (not useRecovery) or st5.flipBuy or st5.flipSell or roll[i] or reg == 0 or na(a) or na(tr5):
            rArm = 0; rBar = None; rTime = None
        else:
            if rArm != 0 and (rArm != reg or rtB - rBar > 6 or b.epoch_min[i] - rTime > 30):
                rArm = 0; rBar = None; rTime = None
            fired = False
            if rArm != 0 and rtB > rBar:
                if reg == 1 and c > pH and c > o:
                    recB = True; fired = True; rArm = 0; rBar = None; rTime = None
                elif reg == -1 and c < pL and c < o:
                    recS = True; fired = True; rArm = 0; rBar = None; rTime = None
            if rArm == 0 and not fired:
                if reg == 1 and l <= tr5 + 0.5 * a:
                    rArm = 1; rBar = rtB; rTime = b.epoch_min[i]
                elif reg == -1 and h >= tr5 - 0.5 * a:
                    rArm = -1; rBar = rtB; rTime = b.epoch_min[i]
        sB = st5.flipBuy or recB; sS = st5.flipSell or recS
        if roll[i]:
            sp = hp = rp = 0; sb = hb = rb = None
        else:
            if sp != 0 and rtB - sb > maxGap: sp = 0; sb = None
            if hp != 0 and rtB - hb > maxGap: hp = 0; hb = None
            if rp != 0 and rtB - rb > maxGap: rp = 0; rb = None
            upE = sB or hmaBuy or rsiBuy; dnE = sS or hmaSell or rsiSell
            if upE and dnE:
                sp = hp = rp = 0; sb = hb = rb = None
            else:
                se = 1 if sB else (-1 if sS else 0); he = 1 if hmaBuy else (-1 if hmaSell else 0); re = 1 if rsiBuy else (-1 if rsiSell else 0)
                ed = se if se != 0 else (he if he != 0 else re)
                if ed != 0:
                    if sp != 0 and sp != ed: sp = 0; sb = None
                    if hp != 0 and hp != ed: hp = 0; hb = None
                    if rp != 0 and rp != ed: rp = 0; rb = None
                if se != 0: sp = se; sb = rtB
                if he != 0: hp = he; hb = rtB
                if re != 0: rp = re; rb = rtB
                if sp != 0 and sp == hp and sp == rp:
                    mb[i] = sp == 1; ms[i] = sp == -1
                    sp = hp = rp = 0; sb = hb = rb = None
        pC, pH, pL, pFast, pSlow = c, h, l, fast, slow
        vw = cumPV / cumV if cumV > 0 else (h + l + c) / 3
        for k, val in dict(atr=a, trail=tr5, regime=reg, htf15=htf15, htf60=htf60, fast=fast, slow=slow, adx=adx, dip=dip, dim=dim,
                           er10=f_er(cBuf, 10), er20=f_er(cBuf, 20), er40=f_er(cBuf, 40), hslope=hslope, ret6=f_diff(cBuf, 6),
                           ret24=f_diff(cBuf, 24), vwap=vw, atrbase=atrBase, volbase=volBase, barOfDay=barOfDay,
                           gap=dayOpen - prevC, daypos=(c - runLo) / (runHi - runLo) if runHi > runLo else 0.5,
                           fromopen=c - dayOpen, prevday=prevC - prevPrevC).items():
            out[k][i] = val
    out["match_buy"] = mb; out["match_sell"] = ms
    return out
