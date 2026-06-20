"""
Reporting and visualization (Section 4.7 / Section 9). Generates the text
performance report, equity-curve / regime / trade-distribution charts, and CSV
trade & signal logs.
"""

import os
from typing import List, Dict
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from strategy_02_queue_depletion.config import OUTPUT_DIR
from strategy_02_queue_depletion.backtest import (
    Trade, compute_trade_statistics, compute_equity_metrics,
)


def generate_performance_report(df: pd.DataFrame, trades: List[Trade]) -> str:
    ts = compute_trade_statistics(trades, df)
    eq = compute_equity_metrics(df, trades)
    exit_lines = "\n".join(f"  {k}: {v}" for k, v in ts.get('exit_reasons', {}).items())
    return f"""
{'='*70}
STRATEGY 2 PERFORMANCE REPORT
Queue-Depletion Momentum with Liquidity Regime Filter
{'='*70}

TRADE STATISTICS
----------------
Total Trades:           {ts['total_trades']}
Long Trades:            {ts['long_trades']}
Short Trades:           {ts['short_trades']}
Win Rate:               {ts['win_rate']*100:.2f}%
Profit Factor:          {ts['profit_factor']:.3f}
Payoff Ratio:           {ts['payoff_ratio']:.3f}

P&L SUMMARY
-----------
Total Net P&L:          ${ts['total_net_pnl']:,.2f}
Total Gross P&L:        ${ts['total_gross_pnl']:,.2f}
Total Costs:            ${ts['total_costs']:,.2f}
Avg P&L per Trade:      ${ts['avg_pnl_per_trade']:.2f}
Median P&L:             ${ts['median_pnl']:.2f}

WIN/LOSS BREAKDOWN
------------------
Winning Trades:         {ts['winning_trades']}
Losing Trades:          {ts['losing_trades']}
Avg Win:                ${ts['avg_win']:.2f}
Avg Loss:               ${ts['avg_loss']:.2f}

REGIME PERFORMANCE
------------------
Tight-Deep Accuracy:    {ts.get('tight_deep_accuracy', 0)*100:.2f}% ({ts.get('tight_deep_trades', 0)} trades)
Wide-Thin Accuracy:     {ts.get('wide_thin_accuracy', 0)*100:.2f}% ({ts.get('wide_thin_trades', 0)} trades)
Disrupted Trades:       {ts.get('disrupted_trades', 0)}

TRADE EXECUTION
---------------
Avg Bars Held:          {ts['avg_bars_held']:.2f}
Trades per Day:         {ts['trades_per_day']:.2f}
Avg MAE (points):       {ts['avg_mae']:.4f}
Avg MFE (points):       {ts['avg_mfe']:.4f}

EQUITY METRICS
--------------
Final Equity:           ${eq['final_equity']:,.2f}
Total Return:           {eq['total_return_pct']:.2f}%
Max Drawdown:           {eq['max_drawdown_pct']:.2f}%
Sharpe Ratio:           {eq['sharpe_ratio']:.3f}
Sortino Ratio:          {eq['sortino_ratio']:.3f}
Calmar Ratio:           {eq['calmar_ratio']:.3f}

EXIT REASONS
------------
{exit_lines}
{'='*70}
"""


def plot_equity_curve(df: pd.DataFrame, output_path: str = None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})
    x = pd.to_datetime(df['ts_event'])
    ax1.plot(x, df['equity'], color='#1f6feb', lw=1.0)
    ax1.set_title("Strategy 2 — Equity Curve (Test Set)")
    ax1.set_ylabel("Equity ($)")
    ax1.grid(alpha=0.3)
    if 'drawdown_pct' in df:
        ax2.fill_between(x, df['drawdown_pct'], 0, color='#d1242f', alpha=0.4)
    ax2.set_ylabel("Drawdown (%)")
    ax2.set_xlabel("Time")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    path = output_path or os.path.join(OUTPUT_DIR, "strategy_02_equity_curve.png")
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return path


def plot_regime_performance(trades: List[Trade], output_path: str = None):
    regimes = {0: 'Tight-Deep', 1: 'Wide-Thin'}
    names, accs, counts = [], [], []
    for r, nm in regimes.items():
        rt = [t for t in trades if t.entry_regime == r]
        names.append(nm)
        accs.append(100 * np.mean([t.net_pnl > 0 for t in rt]) if rt else 0)
        counts.append(len(rt))
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(names, accs, color=['#1f6feb', '#bf8700'])
    ax.axhline(50, color='gray', ls='--', lw=1)
    ax.set_ylabel("Win Rate (%)")
    ax.set_title("Win Rate by Liquidity Regime")
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"n={c}", ha='center')
    ax.grid(alpha=0.3, axis='y')
    fig.tight_layout()
    path = output_path or os.path.join(OUTPUT_DIR, "strategy_02_regime_performance.png")
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return path


def plot_trade_distribution(trades: List[Trade], output_path: str = None):
    pnls = [t.net_pnl for t in trades]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(pnls, bins=60, color='#1f6feb', alpha=0.8, edgecolor='white')
    ax.axvline(0, color='#d1242f', ls='--', lw=1)
    ax.set_xlabel("Net P&L per Trade ($)")
    ax.set_ylabel("Frequency")
    ax.set_title("Trade P&L Distribution")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = output_path or os.path.join(OUTPUT_DIR, "strategy_02_trade_distribution.png")
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return path


def plot_monthly_returns(df: pd.DataFrame, trades: List[Trade], output_path: str = None):
    path = output_path or os.path.join(OUTPUT_DIR, "strategy_02_monthly_returns.png")
    if not trades:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, "No trades", ha='center', va='center')
        fig.savefig(path, dpi=100)
        plt.close(fig)
        return path

    rows = []
    for t in trades:
        ts = pd.Timestamp(t.exit_time).tz_convert('America/New_York')
        rows.append({'year': ts.year, 'month': ts.month, 'pnl': t.net_pnl})
    s = pd.DataFrame(rows)
    piv = s.groupby(['year', 'month'])['pnl'].sum().unstack(fill_value=np.nan)
    piv = piv.reindex(columns=range(1, 13))

    vmax = np.nanmax(np.abs(piv.values)) if np.isfinite(piv.values).any() else 1.0
    fig, ax = plt.subplots(figsize=(12, 1.2 + 0.6 * len(piv)))
    im = ax.imshow(piv.values, cmap='RdYlGn', vmin=-vmax, vmax=vmax, aspect='auto')
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_names)
    ax.set_yticks(range(len(piv)))
    ax.set_yticklabels([str(y) for y in piv.index])
    ax.set_title("Monthly Net P&L Heatmap (Test Set)")
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            if np.isfinite(v):
                ax.text(j, i, f"{v:,.0f}", ha='center', va='center', fontsize=7,
                        color='black')
    fig.colorbar(im, ax=ax, label="Net P&L ($)", fraction=0.025)
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return path


def trades_to_dataframe(trades: List[Trade]) -> pd.DataFrame:
    return pd.DataFrame([{
        'entry_idx': t.entry_idx, 'exit_idx': t.exit_idx,
        'entry_time': t.entry_time, 'exit_time': t.exit_time,
        'direction': t.direction, 'entry_price': t.entry_price, 'exit_price': t.exit_price,
        'entry_regime': t.entry_regime, 'num_contracts': t.num_contracts,
        'gross_pnl': t.gross_pnl, 'net_pnl': t.net_pnl, 'bars_held': t.bars_held,
        'exit_reason': t.exit_reason, 'mae': t.max_adverse_excursion,
        'mfe': t.max_favorable_excursion,
    } for t in trades])


def save_all_reports(df: pd.DataFrame, trades: List[Trade], output_dir: str = OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    report = generate_performance_report(df, trades)
    with open(os.path.join(output_dir, "strategy_02_performance_report.txt"), "w") as f:
        f.write(report)
    plot_equity_curve(df)
    plot_regime_performance(trades)
    plot_trade_distribution(trades)
    plot_monthly_returns(df, trades)
    trades_to_dataframe(trades).to_csv(
        os.path.join(output_dir, "strategy_02_test_trades.csv"), index=False)
    sig_cols = [c for c in ['ts_event', 'close', 'f_liquidity_regime',
                            'sig_direction', 'sig_strength', 'sig_regime', 'sig_action',
                            'position', 'realized_pnl', 'equity'] if c in df.columns]
    if sig_cols:
        df[sig_cols].to_csv(
            os.path.join(output_dir, "strategy_02_test_signals.csv"), index=False)
    return report
