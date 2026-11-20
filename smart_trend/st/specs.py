"""Contract specifications and portfolio groupings."""

SPECS = {
    # symbol: tick size, $ per point, correlation group
    "ES":  dict(tick=0.25, pv=50.0,  group="index"),
    "MES": dict(tick=0.25, pv=5.0,   group="index"),
    "NQ":  dict(tick=0.25, pv=20.0,  group="index"),
    "MNQ": dict(tick=0.25, pv=2.0,   group="index"),
    "YM":  dict(tick=1.0,  pv=5.0,   group="index"),
    "MYM": dict(tick=1.0,  pv=0.5,   group="index"),
    "RTY": dict(tick=0.1,  pv=50.0,  group="index"),
    "M2K": dict(tick=0.1,  pv=5.0,   group="index"),
    "GC":  dict(tick=0.1,  pv=100.0, group="metal"),
    "MGC": dict(tick=0.1,  pv=10.0,  group="metal"),
    "SI":  dict(tick=0.005, pv=5000.0, group="metal"),
    "SIL": dict(tick=0.005, pv=1000.0, group="metal"),
    "CL":  dict(tick=0.01, pv=1000.0, group="energy"),
    "MCL": dict(tick=0.01, pv=100.0, group="energy"),
}

COMMISSION_RT = 2.50   # $ per contract round turn (matches the Pine script: 1.25 per side)
SLIPPAGE_TICKS = 1     # matches the Pine script
