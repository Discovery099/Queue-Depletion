"""Genome -> one self-contained Pine v6 strategy (SPEC 18.1, 18.2).

The signal section is emitted from the same expression trees the Python engine evaluates
(genome/compile_py.build), so the two cannot drift apart.  The order section mirrors the default
engine: decisions on confirmed bars, fills on the next bar, a hard stop with every entry, flat by the
session's last bar.  The owner's "06 Webhook / Live Gates" group is carried over with the same
inputs, payload fields and gate; stop and target exits also send CLOSE_ payloads.

Nothing here connects to a broker or a webhook, and the defaults stay on paper (Article 23).
"""
import math

from genome import compile_py, genome as GN
from genome.dsl import Pine
from library.atoms.catalog import ATOMS, FAMILIES

ETYPE_ARG = {"market": "", "limit": ", limit = {ref}", "stop": ", stop = {ref}"}


def _c(text, width=92):
    out = []
    for para in text.split("\n"):
        line = "//"
        for word in para.split(" "):
            if len(line) + len(word) + 1 > width:
                out.append(line)
                line = "//  " + word if para.startswith("  ") else "// " + word
            else:
                line += " " + word
        out.append(line)
    return out


def export(g, meta=None):
    """meta: optional {'name', 'generation', 'tier', 'win_rate_statement' (text), 'tag'}."""
    meta = meta or {}
    gid = g["genome_id"][:10]
    name = meta.get("name", f"SEH {gid}")
    tag = meta.get("tag", f"SEH_{gid.upper()}")
    x = compile_py.build(g)
    P = Pine()
    sig = {}
    for side in ("long", "short"):
        for k in ("sig", "ref", "stp", "ex"):
            sig[k + side], _ = P.em(x[k][side])
        sig["tgt" + side] = P.em(x["tgt"][side])[0] if x["tgt"][side] is not None else "na"
    sc = x["scalars"]
    ent = g["slots"]["entry"]
    q = g["sequencing"]
    uses_other = any("request.security(otherSymbol" in ln for ln in P.lines)
    atoms = [e["atom"] for e in GN.atom_entries(g)]
    L = []
    L += _c(f"{name}  -  Strategy Evolution Harness export")
    L += _c(f"Generation: {meta.get('generation', 'n/a')}    Tier: {meta.get('tier', 'none (not certified)')}    Genome: {g['genome_id']}")
    L.append("//")
    L += _c("WHAT THIS IS")
    for ln in GN.describe(g).split("\n"):
        L += _c("  " + ln)
    L.append("//")
    if meta.get("win_rate_statement"):
        for ln in meta["win_rate_statement"].split("\n"):
            L.append("//   " + ln)
        L.append("//")
    L += _c("ATOMS (techniques) USED")
    for a in atoms:
        L += _c(f"  {a}: {ATOMS[a].desc} [{FAMILIES[ATOMS[a].fam]}]")
    L += _c("All code in this file is an original implementation of these concepts. No library script text is copied.")
    L.append("//")
    L += _c("CHANGES FROM THE OWNER'S ORIGINAL SCRIPT, AND WHY")
    L += _c("  1. Orders are placed on confirmed bars and fill on the NEXT bar (process_orders_on_close=false). The original filled at the "
            "signal bar's close, a price that cannot be traded once the bar has closed; every research result was measured with next-bar fills.")
    L += _c("  2. Every entry has a hard stop placed with it (strategy.exit). The original had no stop.")
    L += _c("  3. All positions are closed by the session's last regular-hours bar. The original held overnight.")
    L += _c("  4. Stop and target exits send CLOSE_LONG / CLOSE_SHORT payloads through alert_message with their own keys. The original strategy "
            "had no such exits: VERIFY THE SERVER-SIDE HANDLING OF THESE EXITS IN PAPER MODE before anything else.")
    L.append("//")
    L += _c("LIMITS OF THE EVIDENCE")
    L += _c("  Research used two highly correlated instruments (ES, YM), regular trading hours only, 5-minute bars whose intrabar order of "
            "events is unknown, about six years of history and no live fills. TradingView's own fill model is more optimistic than the "
            "research engine's (which assumes the stop fills before the target when both are inside one bar). Use a regular-hours chart. "
            "Session logic assumes the 09:30 to 16:00 Eastern session; on shortened holiday sessions this script cannot know the bar is the "
            "last one, so it flattens at the first bar of the next session instead. Timeframes below 5 minutes were never tested. "
            "No backtest result is a promise of live performance, and nothing here is financial advice.")
    L.append("")
    L.append("//@version=6")
    L.append(f'strategy("{name}", overlay = true, initial_capital = 100000, margin_long = 0, margin_short = 0, '
             "default_qty_type = strategy.fixed, default_qty_value = 1, pyramiding = 0, "
             "commission_type = strategy.commission.cash_per_contract, commission_value = 1.25, slippage = 1, "
             "process_orders_on_close = false, calc_on_every_tick = false)")
    L.append("")
    L += ['// ---- 06 Webhook / Live Gates (carried over from the owner\'s script, same behaviour)',
          'gAlerts = "06 Webhook / Live Gates"',
          'executionMode  = input.string("Sim/Paper", "Execution mode", options = ["Backtest only", "Sim/Paper", "Live"], group = gAlerts, '
          'tooltip = "Backtest only disables all orders and therefore all alerts. Sim/Paper and Live both place orders; the live flag in the JSON tells your server which path to route.")',
          'webhookMode    = input.string("internal_paper", "Webhook mode", options = ["disabled", "internal_paper", "projectx_sim", "live"], group = gAlerts)',
          'acceptLiveRisk = input.bool(false, "I accept full live-trading risk", group = gAlerts)',
          f'alertTag       = input.string("{tag}", "Alert tag", group = gAlerts, tooltip = "A tag of its own so your dashboard can tell strategies apart.")',
          'brokerRoot     = input.string("YM", "Broker root override", group = gAlerts)',
          'tvSymbol       = input.string("CBOT_MINI_DL:YM1!", "TV symbol override", group = gAlerts)',
          'qty            = input.int(4, "Quantity", minval = 1, maxval = 10, group = gAlerts, tooltip = "Contracts per position. Research used 1 contract; sizing is your decision.")',
          'f_num(x) => na(x) ? "null" : str.tostring(x, "#.#####")',
          'f_bool(x) => x ? "true" : "false"',
          'liveAuthorized = executionMode == "Live" and webhookMode == "live" and acceptLiveRisk',
          'ordersOk       = executionMode == "Sim/Paper" or executionMode == "Live"',
          'f_alert(eventName, side, action) =>',
          '    key = syminfo.ticker + "_" + str.tostring(time) + "_" + eventName + "_" + side',
          '    "{" + "\\"action\\":\\"" + action + "\\",\\"side\\":\\"" + side + "\\",\\"qty\\":" + str.tostring(qty) + ",\\"symbol\\":\\"" + tvSymbol + '
          '"\\",\\"broker_root\\":\\"" + brokerRoot + "\\",\\"price\\":" + f_num(close) + ",\\"key\\":\\"" + key + "\\",\\"tag\\":\\"" + alertTag + '
          '"\\",\\"live\\":" + f_bool(liveAuthorized) + "}"', ""]
    L += ['// ---- Strategy settings (units in the tooltips)', 'gRisk = "01 Risk and sequencing"',
          f'cooldownMin = input.int({q["cooldown_minutes"]}, "Cool-down after a loss (minutes)", minval = 0, group = gRisk, '
          'tooltip = "After a losing trade, no new entry in the same direction for this many minutes (at least 2 bars).")',
          f'maxTrades   = input.int({q["max_trades_per_session"]}, "Maximum trades per session", minval = 1, maxval = 6, group = gRisk)',
          f'standDownN  = input.int({q["loss_standdown"]}, "Stand down after this many straight losses in a session", minval = 0, group = gRisk)']
    if uses_other:
        L.append('otherSymbol = input.symbol("CBOT_MINI:ES1!", "Companion instrument", group = gRisk, tooltip = "The other index future (ES when trading YM, YM when trading ES).")')
    L += ["", "// ---- Signal layer: every value is final at the close of the bar it is read on"]
    L += P.lines
    L += ["", "// ---- Order layer", "isLastBar    = mso >= 390.0", "cooldownBars = math.max(2, math.ceil(cooldownMin / tfMin))"]
    if ent["type"] != "market":
        L.append(f"validBars    = math.max(1, math.floor({ent['valid_minutes']}.0 / tfMin + 0.5))")
    if sc["time_stop_minutes"]:
        L.append(f"timeStopBars = math.max(1, math.floor({sc['time_stop_minutes']}.0 / tfMin + 0.5))")
    L += ["var int   tradesToday = 0", "var int   consecLoss  = 0", "var bool  standDown   = false", "var int   lastLossDir = 0",
          "var int   lastLossBar = -1000000", "var float npAtFlat    = 0.0", "var float curStop     = na", "var float curTgt      = na",
          "var float riskPts     = na", "var float mfe         = 0.0", "var int   ordBar      = na", "var bool  tookPartial = false",
          "if newSess", "    tradesToday := 0", "    consecLoss  := 0", "    standDown   := false",
          "posSize   = strategy.position_size", "inLong    = posSize > 0", "inShort   = posSize < 0",
          "tradeDone = strategy.closedtrades > strategy.closedtrades[1] and posSize == 0",
          "enteredNow = (posSize != 0 and strategy.opentrades.entry_bar_index(strategy.opentrades - 1) == bar_index) or "
          "(tradeDone and strategy.closedtrades.entry_bar_index(strategy.closedtrades - 1) == bar_index)",
          "if enteredNow", "    tradesToday += 1", "    mfe := 0.0", "    tookPartial := false",
          "if tradeDone", "    tradeNet = strategy.netprofit - npAtFlat", "    npAtFlat := strategy.netprofit",
          "    if tradeNet > syminfo.mintick * syminfo.pointvalue * qty", "        consecLoss := 0", "    else",
          "        consecLoss  += 1", "        lastLossDir := strategy.closedtrades.size(strategy.closedtrades - 1) > 0 ? 1 : -1",
          "        lastLossBar := bar_index", "        if standDownN > 0 and consecLoss >= standDownN", "            standDown := true",
          "canTrade = barstate.isconfirmed and ordersOk", ""]
    # position management
    L += ["// manage the open position: the stop may only tighten", "if canTrade and posSize != 0",
          "    entryPx = strategy.position_avg_price",
          "    if enteredNow", "        riskPts := math.max(math.abs(entryPx - curStop), syminfo.mintick)",
          "    mfe := math.max(mfe, inLong ? high - entryPx : entryPx - low)"]
    if sc["be_R"]:
        L += [f"    if mfe >= {sc['be_R']} * riskPts", "        curStop := inLong ? math.max(curStop, entryPx) : math.min(curStop, entryPx)"]
    if sc["trail_R"]:
        L += [f"    if mfe >= {sc['trail_start_R']} * riskPts",
              f"        curStop := inLong ? math.max(curStop, entryPx + mfe - {sc['trail_R']} * riskPts) : math.min(curStop, entryPx - mfe + {sc['trail_R']} * riskPts)"]
    if sc["part_R"]:
        L += [f"    t1 = inLong ? entryPx + {sc['part_R']} * riskPts : entryPx - {sc['part_R']} * riskPts",
              "    if not tookPartial and (inLong ? high > t1 : low < t1)", "        tookPartial := true",
              "        curStop := inLong ? math.max(curStop, entryPx) : math.min(curStop, entryPx)",
              '    if not tookPartial', '        strategy.exit(inLong ? "XL1" : "XS1", inLong ? "L" : "S", qty_percent = 50, limit = t1, stop = curStop, '
              'comment = inLong ? "XL" : "XS", alert_message = f_alert("partial", inLong ? "long" : "short", inLong ? "CLOSE_LONG" : "CLOSE_SHORT"))']
    L += ['    strategy.exit(inLong ? "XL" : "XS", inLong ? "L" : "S", stop = curStop, limit = curTgt, comment = inLong ? "XL" : "XS", '
          'alert_message = f_alert("exit", inLong ? "long" : "short", inLong ? "CLOSE_LONG" : "CLOSE_SHORT"))']
    disc = f"(inLong and {sig['exlong']}) or (inShort and {sig['exshort']})"
    if sc["time_stop_minutes"]:
        disc += " or (bar_index - strategy.opentrades.entry_bar_index(0) + 1 >= timeStopBars)"
    L += [f"    if {disc}", '        strategy.close(inLong ? "L" : "S", comment = inLong ? "XL" : "XS", '
          'alert_message = f_alert("exit_rule", inLong ? "long" : "short", inLong ? "CLOSE_LONG" : "CLOSE_SHORT"))',
          "    if isLastBar", '        strategy.close_all(immediately = true, comment = inLong ? "XL" : "XS", '
          'alert_message = f_alert("session", inLong ? "long" : "short", inLong ? "CLOSE_LONG" : "CLOSE_SHORT"))', ""]
    # entries
    L += ["// new entries: flat, not the session's last bar, limits respected",
          "wantL = " + sig["siglong"] + " and not " + sig["sigshort"] + " and not (lastLossDir == 1 and bar_index - lastLossBar < cooldownBars)",
          "wantS = " + sig["sigshort"] + " and not " + sig["siglong"] + " and not (lastLossDir == -1 and bar_index - lastLossBar < cooldownBars)",
          "if canTrade and posSize == 0"]
    if ent["type"] != "market":
        L += ["    if not na(ordBar) and bar_index - ordBar >= validBars", "        strategy.cancel_all()", "        ordBar := na"]
    L += ["    if isLastBar", "        strategy.cancel_all()", "    else if not standDown and tradesToday < maxTrades"]
    for side, d, eid, xid, act in (("long", "strategy.long", "L", "XL", "BUY"), ("short", "strategy.short", "S", "XS", "SELL_SHORT")):
        want = "wantL" if side == "long" else "wantS"
        arg = ETYPE_ARG[ent["type"]].format(ref=sig["ref" + side])
        L += [f"        if {want}", "            strategy.cancel_all()",
              f"            curStop := {sig['stp' + side]}", f"            curTgt  := {sig['tgt' + side]}", "            ordBar  := bar_index",
              f'            strategy.entry("{eid}", {d}, qty = qty{arg}, comment = "{eid}", alert_message = f_alert("entry", "{side}", "{act}"))',
              f'            strategy.exit("{xid}", "{eid}", stop = curStop, limit = curTgt, comment = "{xid}", '
              f'alert_message = f_alert("exit", "{side}", "CLOSE_{side.upper()}"))']
    L += ["// safety: a position carried past an unrecognised short session is closed on the next session's first bar",
          "if canTrade and newSess and posSize != 0",
          '    strategy.close_all(comment = inLong ? "XL" : "XS", alert_message = f_alert("carry", inLong ? "long" : "short", inLong ? "CLOSE_LONG" : "CLOSE_SHORT"))', ""]
    L += ["// ---- Visuals (do not affect orders)",
          f'plotshape({sig["siglong"]} and posSize == 0, title = "Long setup", location = location.belowbar, color = color.new(#00D084, 0), style = shape.triangleup, size = size.tiny)',
          f'plotshape({sig["sigshort"]} and posSize == 0, title = "Short setup", location = location.abovebar, color = color.new(#FF4757, 0), style = shape.triangledown, size = size.tiny)',
          'plot(posSize != 0 ? curStop : na, title = "Stop", color = color.new(#FF4757, 0), style = plot.style_linebr)',
          'plot(posSize != 0 ? curTgt : na, title = "Target", color = color.new(#00D084, 0), style = plot.style_linebr)',
          "var table info = table.new(position.top_right, 2, 5, bgcolor = color.new(color.black, 10), frame_width = 1, frame_color = color.gray)",
          "if barstate.islast",
          f'    table.cell(info, 0, 0, "{name}", text_color = color.white, text_size = size.small)',
          '    table.cell(info, 1, 0, "", text_color = color.white, text_size = size.small)',
          '    table.cell(info, 0, 1, "Position", text_color = color.gray, text_size = size.tiny)',
          '    table.cell(info, 1, 1, posSize > 0 ? "LONG" : posSize < 0 ? "SHORT" : "FLAT", text_color = color.white, text_size = size.tiny)',
          '    table.cell(info, 0, 2, "Trades today", text_color = color.gray, text_size = size.tiny)',
          '    table.cell(info, 1, 2, str.tostring(tradesToday), text_color = color.white, text_size = size.tiny)',
          '    table.cell(info, 0, 3, "Stood down", text_color = color.gray, text_size = size.tiny)',
          '    table.cell(info, 1, 3, standDown ? "yes" : "no", text_color = color.white, text_size = size.tiny)',
          '    table.cell(info, 0, 4, "Gate", text_color = color.gray, text_size = size.tiny)',
          '    table.cell(info, 1, 4, liveAuthorized ? "LIVE AUTH" : "sim/paper", text_color = liveAuthorized ? color.red : color.white, text_size = size.tiny)', ""]
    L += _c("ALERT SETUP (unchanged from the owner's script): create ONE alert on this strategy, condition 'Order fills only', "
            "message {{strategy.order.alert_message}} and nothing else, webhook = your own URL. No URL is embedded here and the defaults are paper.")
    return "\n".join(L) + "\n"
