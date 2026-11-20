"""Equity-curve chart: original script vs enhanced portfolio (MES+MNQ+YM, 2022-01 .. 2026-03)."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
TZ = "America/New_York"
O = pd.read_csv(os.path.join(OUT, "original_portfolio_trades.csv"))
O["exit_time"] = pd.to_datetime(O.exit_time, utc=True).dt.tz_convert(TZ)
E = pd.read_csv(os.path.join(OUT, "final_portfolio_trades.csv"), parse_dates=["exit_time"])
E["exit_time"] = pd.to_datetime(E.exit_time, utc=True).dt.tz_convert(TZ)

INK, INK2, MUTED, GRID, BASE, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUE, ORANGE = "#2a78d6", "#eb6834"
fig, axes = plt.subplots(2, 1, figsize=(11, 7.2), dpi=150, sharex=True,
                         gridspec_kw=dict(height_ratios=[3, 1.3], hspace=0.12))
fig.patch.set_facecolor(SURF)
for ax in axes:
    ax.set_facecolor(SURF)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(BASE)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def curve(T):
    T = T.sort_values("exit_time")
    eq = T.pnl.cumsum().to_numpy()
    return T.exit_time.dt.tz_localize(None).to_numpy(), eq


for T, col, lab in ((E, BLUE, "Enhanced"), (O, ORANGE, "Original")):
    x, eq = curve(T)
    axes[0].plot(x, eq, color=col, linewidth=2, solid_capstyle="round")
    axes[0].annotate(f"{lab}  {eq[-1]:+,.0f}", xy=(x[-1], eq[-1]), xytext=(6, 0), textcoords="offset points",
                     va="center", fontsize=10, color=INK)
    dd = eq - np.maximum.accumulate(np.maximum(eq, 0))
    axes[1].plot(x, dd, color=col, linewidth=1.6)
axes[0].axhline(0, color=BASE, linewidth=1)
axes[0].axvline(np.datetime64("2024-01-01"), color=MUTED, linewidth=0.8, linestyle=(0, (3, 3)))
axes[0].text(np.datetime64("2024-01-15"), axes[0].get_ylim()[1] * 0.92, "confirmation period →", color=INK2, fontsize=9)
axes[0].set_ylabel("Cumulative net P&L, USD", color=INK2, fontsize=9)
axes[1].set_ylabel("Drawdown, USD", color=INK2, fontsize=9)
axes[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
axes[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
axes[0].legend(handles=[plt.Line2D([], [], color=BLUE, lw=2, label="Enhanced, preset S1 + portfolio guard"),
                        plt.Line2D([], [], color=ORANGE, lw=2, label="Original script")],
               loc="upper left", frameon=False, fontsize=9, labelcolor=INK)
fig.suptitle("6 MES + 5 MNQ + 1 YM, out-of-sample 2022-01 to 2026-03 (RTH, realistic fills)",
             x=0.01, ha="left", fontsize=12, color=INK)
fig.savefig(os.path.join(OUT, "equity_curve.png"), bbox_inches="tight", facecolor=SURF)
print("saved", O.pnl.sum(), E.pnl.sum())
