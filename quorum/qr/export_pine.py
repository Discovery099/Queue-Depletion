"""Writes deliverables/SmartTrend_Quorum.pine: Smart Trend V1 as the base, library techniques as voters, the
agreement window, one exit family, and the owner's webhook group.  Voter formulas come from the same DSL
expressions the research engine evaluated (emitter verified against an independent interpreter in harness/)."""
import json
import os

import numpy as np

from . import search as Q
from .common import ROOT, F, SYMS
from .report import full, words
from library.atoms import catalog as CAT
from genome.dsl import Pine

fin = json.load(open(os.path.join(ROOT, "reports", "phase4.json")))["finalists"][0]
g = fin["g"]
g["exit"] = tuple(g["exit"])
e = Q.env(5)
names, ids, params = e["names"], e["ids"], e["params"]
default_on = [names[v] for v in g["panel"]]
EXTRA = ["supertrend_flip", "ema_cross", "macd_signal_cross", "rsi_midline_cross", "donchian_break", "roc_thrust",
         "bollinger_break", "keltner_break", "cci_breakout", "range_expansion_break", "two_bar_reversal", "stochastic_cross"]
voters = default_on + [n for n in EXTRA if n not in default_on]
LABEL = {"squeeze_release": "Squeeze release (Bollinger leaves Keltner)", "wick_rejection[n=5]": "Wick rejection at a 5-bar extreme",
         "hma_turn[n=49]": "Hull average (49) turns", "volume_dryup_extreme": "New 20-bar extreme on low volume, reversal",
         "supertrend_flip": "Supertrend (14, 3) flips", "ema_cross": "EMA 13 crosses EMA 55", "macd_signal_cross": "MACD crosses its signal",
         "rsi_midline_cross": "RSI (14) crosses 50", "donchian_break": "Donchian (40) breakout", "roc_thrust": "Momentum thrust (8 bars > 2 ATR)",
         "bollinger_break": "Close beyond Bollinger (30, 2)", "keltner_break": "Close beyond Keltner (30, 1.5)", "cci_breakout": "CCI (20) beyond 100",
         "range_expansion_break": "Widest bar of 10 breaks the range", "two_bar_reversal": "Two-bar reversal", "stochastic_cross": "Stochastic %K crosses %D"}

P = Pine()
vn = []
for nm in voters:
    v = names.index(nm)
    ex = CAT.ATOMS[ids[v]].build(params[v])
    L, _ = P.em(ex["long"])
    Sx, _ = P.em(ex["short"])
    vn.append((nm, L, Sx))

# ---- self-check of the agreement logic as it is written in Pine (barssince form) against the research engine
c = e["ES"]
bs = c["base"][g["factor"]]
W, m = g["W"], g["m"]
cL = np.zeros(c["b"].n, int); cS = cL.copy(); nowL = np.zeros(c["b"].n, bool); nowS = nowL.copy()
for v in g["panel"]:
    eL, eS = c["EV"][v] > 0, c["EV"][v] < 0
    cL += (np.nan_to_num(F.barssince(eL), nan=1e9) <= W); cS += (np.nan_to_num(F.barssince(eS), nan=1e9) <= W)
    nowL |= eL; nowS |= eS
baseL, baseS = (bs["bsL"] <= W, bs["bsS"] <= W) if g["mode"] == "arrow" else (bs["reg"] == 1, bs["reg"] == -1)
okL, okS = (cL >= m) & (cS == 0) & baseL, (cS >= m) & (cL == 0) & baseS
fL, fS = okL & nowL & ~np.r_[False, okL[:-1]], okS & nowS & ~np.r_[False, okS[:-1]]
rL, rS, _ = Q.signals(g, c)
assert (fL == rL).all() and (fS == rS).all(), "Pine-form agreement logic differs from the research engine"
print("agreement logic self-check: identical on", int(rL.sum() + rS.sum()), "ES signals")

ex = g["exit"]
H = []
A = H.append
A("// This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.")
A("// https://mozilla.org/MPL/2.0/")
A("// Smart Trail and arrow logic: Smart Trend V1 (owner's script). Lorentzian engine and kernel adapted from (c) jdehorty,")
A("// in the form used in the owner's 'ARES LC + Smart Trend Sync'. Voter formulas: re-implementations of common library techniques.")
A("//")
A("// SMART TREND QUORUM - research test bench, NOT a validated strategy.")
A("// A trade fires only when the Smart Trend base and at least N other techniques agree within a few candles:")
A("//   base = 'Arrow'  : a Smart Trend arrow, then a voter's signal on the same candle or up to W candles later")
A("//   base = 'Regime' : the Smart Trail is on the trade side and the voters agree within W candles")
A("//   an opposite signal from any switched-on voter inside the window cancels the trade")
A("// Default settings = the best candidate of a 100,000-candidate search on ES and YM 5-minute regular-hours data:")
A(f"//   {words(g, e)}")
d, cf, al = fin["disc"]["pooled"], fin["conf"]["pooled"], fin["all"]["pooled"]
A(f"//   selected on half of 2020-2023: {d['tpd']:.1f} trades/day, {d['wr']:.0f}% wins, profit factor {d['pf']:.2f}")
A(f"//   on the other half (never used for selection): {cf['tpd']:.1f} trades/day, {cf['wr']:.0f}% wins, profit factor {cf['pf']:.2f}")
A("//   That second line is the honest one. It does not meet the goal (5 trades/day, 60% wins, profit factor 2).")
A("// Research fills: next bar open, 1 tick slippage, $1.25 a side, flat at 16:00 New York. Overnight holding was never tested.")
A("// Signals use closed bars only; there is no request.security and no lookahead, so arrows do not repaint.")
A("//@version=6")
A('strategy("Smart Trend Quorum (research test bench)", shorttitle="ST Quorum", overlay=true, initial_capital=100000, margin_long=0, margin_short=0, default_qty_type=strategy.fixed, default_qty_value=1, pyramiding=0, commission_type=strategy.commission.cash_per_contract, commission_value=1.25, slippage=1, process_orders_on_close=false, calc_on_every_tick=false, max_labels_count=500)')
A("")
A("import jdehorty/MLExtensions/2 as ml")
A("import jdehorty/KernelFunctions/2 as kernels")
A("")
A('gBase = "01 Smart Trend base"')
A(f'baseMode   = input.string("{"Arrow" if g["mode"] == "arrow" else "Regime"}", "Base role", options=["Arrow", "Regime"], group=gBase, tooltip="Arrow: a Smart Trend arrow must be followed by the voters within the window. Regime: the Smart Trail must be on the trade side.")')
A('i_atrLen   = input.int(14, "ATR Length", minval=5, maxval=100, group=gBase)')
A(f'i_factor   = input.float({g["factor"]:g}, "Factor", minval=0.5, maxval=5.0, step=0.1, group=gBase, tooltip="Owner default 3.0. Lower = more arrows.")')
A('i_confirm  = input.int(1, "Confirm Bars", minval=1, maxval=3, group=gBase)')
A('i_adaptLen = input.int(10, "Adaptation EMA", minval=1, maxval=30, group=gBase)')
A("")
A('gQ = "02 Agreement"')
A(f'window  = input.int({W}, "Window: candles allowed between signals", minval=0, maxval=10, group=gQ, tooltip="0 = same candle only.")')
A(f'quorumN = input.int({m}, "How many voters must agree", minval=1, maxval=6, group=gQ)')
A("")
A('gV = "03 Voters (switch on the techniques that may vote)"')
for i, (nm, L, Sx) in enumerate(vn):
    A(f'use{i + 1} = input.bool({"true" if nm in default_on else "false"}, "{LABEL[nm]}", group=gV)')
A('useLC = input.bool(false, "Lorentzian classification signal (heavy; off by default)", group=gV)')
A("")
A('gX = "04 Exits"')
A(f'stopAtr  = input.float({ex[1]:g}, "Stop distance (ATR)", minval=0.25, step=0.25, group=gX)')
A(f'targetR  = input.float({ex[2]:g}, "Target (multiple of the stop distance)", minval=0.1, step=0.05, group=gX)')
A(f'halfOffR = input.float({g["part"]:g}, "Take half off at this multiple of the stop distance (0 = off; needs quantity 2 or more)", minval=0.0, step=0.05, group=gX, tooltip="After the half is taken the stop moves to the entry price. The partial exit sends CLOSE_LONG / CLOSE_SHORT with half the quantity; check that your server handles a partial close before using it live.")')
A(f'maxBars  = input.int({ex[3]}, "Exit after this many bars (0 = off)", minval=0, group=gX)')
A('dayOnly  = input.bool(true, "Day session only: flat at 16:00 New York, entries 09:30 to 15:55", group=gX, tooltip="This is how it was tested. Switched off, positions are held overnight - untested.")')
A('maxTrades = input.int(20, "Maximum trades per day", minval=1, group=gX)')
A("")
A('gAlerts = "06 Webhook / Live Gates"')
A('executionMode  = input.string("Sim/Paper", "Execution mode", options=["Backtest only", "Sim/Paper", "Live"], group=gAlerts)')
A('webhookMode    = input.string("internal_paper", "Webhook mode", options=["disabled", "internal_paper", "projectx_sim", "live"], group=gAlerts)')
A('acceptLiveRisk = input.bool(false, "I accept full live-trading risk", group=gAlerts)')
A('alertTag       = input.string("ST_QUORUM", "Alert tag", group=gAlerts)')
A('brokerRoot     = input.string("YM", "Broker root override", group=gAlerts)')
A('tvSymbol       = input.string("CBOT_MINI_DL:YM1!", "TV symbol override", group=gAlerts)')
A('qty            = input.int(4, "Quantity", minval=1, maxval=10, group=gAlerts)')
A('f_num(x) => na(x) ? "null" : str.tostring(x, "#.#####")')
A('f_bool(x) => x ? "true" : "false"')
A('liveAuthorized = executionMode == "Live" and webhookMode == "live" and acceptLiveRisk')
A('ordersOk       = executionMode == "Sim/Paper" or executionMode == "Live"')
A("f_alert(eventName, side, action, q) =>")
A('    key = syminfo.ticker + "_" + str.tostring(time) + "_" + eventName + "_" + side')
A('    "{" + "\\"action\\":\\"" + action + "\\",\\"side\\":\\"" + side + "\\",\\"qty\\":" + str.tostring(q) + ",\\"symbol\\":\\"" + tvSymbol + "\\",\\"broker_root\\":\\"" + brokerRoot + "\\",\\"price\\":" + f_num(close) + ",\\"key\\":\\"" + key + "\\",\\"tag\\":\\"" + alertTag + "\\",\\"live\\":" + f_bool(liveAuthorized) + "}"')
A("")
A("// ---- Smart Trend V1 core (owner's algorithm, unchanged)")
A("""_rawAtr = ta.atr(i_atrLen)
_atr = ta.ema(_rawAtr, i_adaptLen)
_buffer = i_factor * _atr
var float trailLevel = na
var int regime = 0
var int confirmCount = 0
if na(trailLevel) and not na(_atr)
    trailLevel := close
    regime := close > close[1] ? 1 : -1
    confirmCount := 0
if not na(trailLevel) and not na(_buffer)
    float rawTrail = na
    int rawRegime = regime
    if regime == 1
        rawTrail := math.max(trailLevel, close - _buffer)
        if close < rawTrail
            rawRegime := -1
    else
        rawTrail := math.min(trailLevel, close + _buffer)
        if close > rawTrail
            rawRegime := 1
    if rawRegime != regime
        confirmCount += 1
        if confirmCount >= i_confirm
            regime := rawRegime
            confirmCount := 0
            trailLevel := regime == 1 ? close - _buffer : close + _buffer
        else
            trailLevel := regime == 1 ? math.max(trailLevel, close - _buffer) : math.min(trailLevel, close + _buffer)
    else
        confirmCount := 0
        trailLevel := regime == 1 ? math.max(trailLevel, close - _buffer) : math.min(trailLevel, close + _buffer)
buyArrow  = regime == 1 and regime[1] == -1
sellArrow = regime == -1 and regime[1] == 1""")
A("")
A("// ---- Voters from the library (closed-bar formulas; names xN are generated)")
H += P.lines
A("")
A("// ---- Lorentzian voter (from the owner's merged script; runs only when switched on)")
A("""lcF1 = ml.n_rsi(close, 14, 1)
lcF2 = ml.n_wt(hlc3, 10, 11)
lcF3 = ml.n_cci(close, 20, 1)
lcF4 = ml.n_adx(high, low, close, 20)
lcF5 = ml.n_rsi(close, 9, 1)
var array<float> lcA1 = array.new_float()
var array<float> lcA2 = array.new_float()
var array<float> lcA3 = array.new_float()
var array<float> lcA4 = array.new_float()
var array<float> lcA5 = array.new_float()
var array<int> lcLabels = array.new_int()
var array<int> lcPreds = array.new_int()
var array<float> lcDists = array.new_float()
var float lcPrediction = 0.0
var int lcSignal = 0
int lcLabel = close[4] < close ? -1 : close[4] > close ? 1 : 0
if useLC
    array.push(lcA1, lcF1)
    array.push(lcA2, lcF2)
    array.push(lcA3, lcF3)
    array.push(lcA4, lcF4)
    array.push(lcA5, lcF5)
    array.push(lcLabels, lcLabel)
    int lcEnd = array.size(lcLabels) - 1
    int lcStart = math.max(0, lcEnd - 1999)
    float lcLast = -1.0
    for i = lcStart to lcEnd
        float dist = math.log(1 + math.abs(lcF1 - array.get(lcA1, i))) + math.log(1 + math.abs(lcF2 - array.get(lcA2, i))) + math.log(1 + math.abs(lcF3 - array.get(lcA3, i))) + math.log(1 + math.abs(lcF4 - array.get(lcA4, i))) + math.log(1 + math.abs(lcF5 - array.get(lcA5, i)))
        if not na(dist) and dist >= lcLast and i % 4 != 0
            lcLast := dist
            array.push(lcDists, dist)
            array.push(lcPreds, array.get(lcLabels, i))
            if array.size(lcPreds) > 8
                lcLast := array.get(lcDists, 6)
                array.shift(lcDists)
                array.shift(lcPreds)
    lcPrediction := array.sum(lcPreds)
bool lcVolOk = ml.filter_volatility(1, 10, true)
bool lcRegOk = ml.regime_filter(ohlc4, -0.1, true)
lcSignal := lcPrediction > 0 and lcVolOk and lcRegOk ? 1 : lcPrediction < 0 and lcVolOk and lcRegOk ? -1 : nz(lcSignal[1], 0)
bool lcChanged = ta.change(lcSignal) != 0
float lcKernel = kernels.rationalQuadratic(close, 8, 8.0, 25)
bool lcLong  = useLC and lcSignal == 1 and lcChanged and lcKernel > lcKernel[1]
bool lcShort = useLC and lcSignal == -1 and lcChanged and lcKernel < lcKernel[1]""")
A("")
A("// ---- Agreement: each voter's signal stays valid for `window` candles")
allv = []
for i, (nm, L, Sx) in enumerate(vn):
    k = i + 1
    A(f"e{k}L = use{k} and {L} and not {Sx}")
    A(f"e{k}S = use{k} and {Sx} and not {L}")
    A(f"r{k}L = ta.barssince(e{k}L) <= window")
    A(f"r{k}S = ta.barssince(e{k}S) <= window")
    allv.append(str(k))
A("eLcL = lcLong and not lcShort")
A("eLcS = lcShort and not lcLong")
A("rLcL = ta.barssince(eLcL) <= window")
A("rLcS = ta.barssince(eLcS) <= window")
A("cntL = " + " + ".join(f"(r{k}L ? 1 : 0)" for k in allv) + " + (rLcL ? 1 : 0)")
A("cntS = " + " + ".join(f"(r{k}S ? 1 : 0)" for k in allv) + " + (rLcS ? 1 : 0)")
A("nowL = " + " or ".join(f"e{k}L" for k in allv) + " or eLcL")
A("nowS = " + " or ".join(f"e{k}S" for k in allv) + " or eLcS")
A('baseL = baseMode == "Arrow" ? ta.barssince(buyArrow) <= window : regime == 1')
A('baseS = baseMode == "Arrow" ? ta.barssince(sellArrow) <= window : regime == -1')
A("okL = cntL >= quorumN and cntS == 0 and baseL")
A("okS = cntS >= quorumN and cntL == 0 and baseS")
A("fireL = okL and nowL and not okL[1]")
A("fireS = okS and nowS and not okS[1]")
A("")
A("// ---- Orders: entry at the next bar's open; stop and target measured from the signal candle's close")
A("""atrNow = ta.atr(14)
nyMin = hour(time_close, "America/New_York") * 60 + minute(time_close, "America/New_York")
flatNow = dayOnly and (nyMin >= 960 or nyMin <= 570 or session.islastbar_regular)
canEnter = not dayOnly or (nyMin > 570 and nyMin < 960 and not session.islastbar_regular)
var int tradesToday = 0
var int sigBar = na
var float stopPx = na
var float tgtPx = na
var float halfPx = na
if ta.change(time("D")) != 0
    tradesToday := 0
bool usePartial = halfOffR > 0 and qty >= 2
int halfQty = int(math.floor(qty / 2))
isFlat = strategy.position_size == 0
lossNow = strategy.losstrades > strategy.losstrades[1]
lastDir = strategy.closedtrades > 0 ? (strategy.closedtrades.size(strategy.closedtrades - 1) > 0 ? 1 : -1) : 0
goL = fireL and not fireS and isFlat and canEnter and ordersOk and not na(atrNow) and tradesToday < maxTrades and not (lossNow and lastDir == 1)
goS = fireS and not fireL and isFlat and canEnter and ordersOk and not na(atrNow) and tradesToday < maxTrades and not (lossNow and lastDir == -1)
if goL
    stopPx := math.round_to_mintick(close - stopAtr * atrNow)
    tgtPx  := math.round_to_mintick(close + stopAtr * targetR * atrNow)
    halfPx := math.round_to_mintick(close + stopAtr * halfOffR * atrNow)
    sigBar := bar_index
    tradesToday += 1
    strategy.entry("Long", strategy.long, qty=qty, comment="L", alert_message=f_alert("entry", "long", "BUY", qty))
if goS
    stopPx := math.round_to_mintick(close + stopAtr * atrNow)
    tgtPx  := math.round_to_mintick(close - stopAtr * targetR * atrNow)
    halfPx := math.round_to_mintick(close - stopAtr * halfOffR * atrNow)
    sigBar := bar_index
    tradesToday += 1
    strategy.entry("Short", strategy.short, qty=qty, comment="S", alert_message=f_alert("entry", "short", "SELL_SHORT", qty))
// after the half is taken, the stop moves to the entry price
if strategy.position_size > 0 and usePartial and strategy.position_size < qty
    stopPx := math.max(stopPx, strategy.position_avg_price)
if strategy.position_size < 0 and usePartial and -strategy.position_size < qty
    stopPx := math.min(stopPx, strategy.position_avg_price)
if goL or strategy.position_size > 0
    if usePartial and (goL or strategy.position_size == qty)
        strategy.exit("L half", from_entry="Long", qty=halfQty, limit=halfPx, stop=stopPx, comment="XL", alert_message=f_alert("half", "long", "CLOSE_LONG", halfQty))
    strategy.exit("L exit", from_entry="Long", limit=tgtPx, stop=stopPx, comment="XL", alert_message=f_alert("exit", "long", "CLOSE_LONG", qty))
if goS or strategy.position_size < 0
    if usePartial and (goS or -strategy.position_size == qty)
        strategy.exit("S half", from_entry="Short", qty=halfQty, limit=halfPx, stop=stopPx, comment="XS", alert_message=f_alert("half", "short", "CLOSE_SHORT", halfQty))
    strategy.exit("S exit", from_entry="Short", limit=tgtPx, stop=stopPx, comment="XS", alert_message=f_alert("exit", "short", "CLOSE_SHORT", qty))
timeUp = maxBars > 0 and not isFlat and not na(sigBar) and bar_index - sigBar >= maxBars
if timeUp and strategy.position_size > 0
    strategy.close("Long", comment="XL", alert_message=f_alert("time", "long", "CLOSE_LONG", qty))
if timeUp and strategy.position_size < 0
    strategy.close("Short", comment="XS", alert_message=f_alert("time", "short", "CLOSE_SHORT", qty))
if flatNow and strategy.position_size > 0
    strategy.close("Long", comment="XL", immediately=true, alert_message=f_alert("eod", "long", "CLOSE_LONG", qty))
if flatNow and strategy.position_size < 0
    strategy.close("Short", comment="XS", immediately=true, alert_message=f_alert("eod", "short", "CLOSE_SHORT", qty))""")
A("")
A("// ---- Display")
A("""trailColor = regime == 1 ? #00D084 : #FF4757
plot(trailLevel, "Smart Trail", color=trailColor, linewidth=2)
plotshape(buyArrow, title="Smart Trend buy arrow", style=shape.triangleup, location=location.belowbar, color=#00D084, size=size.tiny)
plotshape(sellArrow, title="Smart Trend sell arrow", style=shape.triangledown, location=location.abovebar, color=#FF4757, size=size.tiny)
plotshape(nowL and not fireL, title="Voter buy signal", style=shape.circle, location=location.belowbar, color=color.new(color.aqua, 40), size=size.tiny)
plotshape(nowS and not fireS, title="Voter sell signal", style=shape.circle, location=location.abovebar, color=color.new(color.orange, 40), size=size.tiny)
plotshape(goL, title="Agreed BUY", style=shape.labelup, location=location.belowbar, color=#009988, text="BUY", textcolor=color.white, size=size.small)
plotshape(goS, title="Agreed SELL", style=shape.labeldown, location=location.abovebar, color=#CC3311, text="SELL", textcolor=color.white, size=size.small)
plot(strategy.position_size != 0 ? stopPx : na, "Stop", color=#CC3311, style=plot.style_linebr)
plot(strategy.position_size != 0 ? tgtPx : na, "Target", color=#009988, style=plot.style_linebr)
bgcolor(goL ? color.new(#00D084, 90) : goS ? color.new(#FF4757, 90) : na, title="Agreed entry")
alertcondition(goL or goS, title="Smart Trend Quorum - agreed entry", message="Smart Trend Quorum entry on {{ticker}} @ {{close}}")""")
src = "\n".join(H) + "\n"
open(os.path.join(ROOT, "deliverables", "SmartTrend_Quorum.pine"), "w").write(src)
print("lines", len(H), "voters", len(vn))

# ---- check sheet: ten trades per instrument from the research engine with the default settings
Ts = Q.run(g, e)
import pandas as pd
out = ["# Check sheet: default settings, 5-minute regular-hours chart", "",
       "Times are New York, the open of the candle the trade was entered on. If these entries appear on your chart at these",
       "times and in these directions, the script is doing what the research engine did.", ""]
for sym in SYMS:
    b, T = e[sym]["b"], Ts[sym]
    sel = T[-10:]
    out += [f"## {sym}1!", "", "| Entry candle (New York) | Direction | Entry price | Exit reason |", "|---|---|---|---|"]
    for t in sel:
        ts = pd.Timestamp(int(b.ts[int(t[1])]), tz="UTC").tz_convert("America/New_York")
        out.append(f"| {ts:%Y-%m-%d %H:%M} | {'long' if t[3] > 0 else 'short'} | {t[4]:.2f} | {Q.S.REASONS[int(t[8])]} |")
    out.append("")
open(os.path.join(ROOT, "deliverables", "CHECK_SHEET.md"), "w").write("\n".join(out))
print("\n".join(out[5:22]))
