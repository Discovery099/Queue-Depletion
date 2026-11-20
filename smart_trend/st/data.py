"""Load 5-minute RTH OHLCV files into numpy arrays with New York calendar fields."""
import os
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


class Bars:
    pass


def load(symbol: str, start=None, end=None) -> Bars:
    path = os.path.join(DATA_DIR, f"{symbol}_5min_RTH.csv")
    d = pd.read_csv(path)
    ts = pd.to_datetime(d["ts_event"], utc=True).dt.tz_convert("America/New_York")
    d["ts"] = ts
    if start is not None:
        d = d[d.ts >= pd.Timestamp(start, tz="America/New_York")]
    if end is not None:
        d = d[d.ts < pd.Timestamp(end, tz="America/New_York")]
    d = d.reset_index(drop=True)
    b = Bars()
    b.symbol = symbol
    b.ts = d.ts.values  # numpy datetime64 (UTC-naive repr of NY-aware -> use pandas Series below)
    b.ts_series = d.ts
    b.o = d.open.to_numpy(np.float64)
    b.h = d.high.to_numpy(np.float64)
    b.l = d.low.to_numpy(np.float64)
    b.c = d.close.to_numpy(np.float64)
    b.v = d.volume.to_numpy(np.float64)
    b.n = len(d)
    date = d.ts.dt.date
    b.date = date.values
    b.day_id = pd.factorize(date)[0].astype(np.int64)
    b.minute = (d.ts.dt.hour * 60 + d.ts.dt.minute).to_numpy(np.int64)
    b.month = d.ts.dt.month.to_numpy(np.int64)
    b.dom = d.ts.dt.day.to_numpy(np.int64)
    b.year = d.ts.dt.year.to_numpy(np.int64)
    b.epoch_min = (d.ts.astype("int64") // 60_000_000_000).to_numpy(np.int64)
    # last bar of each session (flatten point; also the bar on which new entries are blocked)
    b.last_bar = np.r_[b.day_id[1:] != b.day_id[:-1], True]
    b.first_bar = np.r_[True, b.day_id[1:] != b.day_id[:-1]]
    # bar number within the session
    b.bar_of_day = d.groupby(b.day_id).cumcount().to_numpy(np.int64)
    # quarterly roll window used by the original script (trading dates 7-22 of Mar/Jun/Sep/Dec)
    b.roll_blocked = np.isin(b.month, [3, 6, 9, 12]) & (b.dom >= 7) & (b.dom <= 22)
    return b
