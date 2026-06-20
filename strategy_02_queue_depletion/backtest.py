"""
Backtesting engine (Section 4). A single tight state-machine core (`_simulate`)
drives both signal generation and the full backtest, guaranteeing consistency.
Transaction costs ($30/round turn) and 1-tick/side slippage are applied once.
"""

from dataclasses import dataclass
from typing import Tuple, List, Dict
import numpy as np
import pandas as pd

from strategy_02_queue_depletion.config import (
    ES_POINT_VALUE, ES_TICK_SIZE, TRANSACTION_COST_PER_TRADE, STARTING_EQUITY,
    ANNUALIZATION, EXIT_REASON_LABELS,
)

_TICK = ES_TICK_SIZE
_PV = ES_POINT_VALUE
_COST = TRANSACTION_COST_PER_TRADE

_ENGINE_COLS = [
    'close', 'high', 'low', 'bar_in_day', 'f_atr_20', 'f_liquidity_regime',
    'f_depletion_ma_5', 'f_toxicity_ma_5', 'f_momentum_3', 'f_momentum_6',
    'f_ema_diff', 'f_depletion_diff', 'f_bar_range', 'f_atr_20_pct',
    'f_volume_ratio', 'f_position_scale', 'tmp_vol_pctile_100',
]


@dataclass
class Trade:
    entry_idx: int
    exit_idx: int
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: int
    entry_price: float
    exit_price: float
    entry_regime: int
    num_contracts: int
    gross_pnl: float
    net_pnl: float
    bars_held: int
    exit_reason: str
    max_adverse_excursion: float
    max_favorable_excursion: float


def extract_arrays(df: pd.DataFrame) -> Dict[str, np.ndarray]:
    """Extract numpy arrays needed by the simulation core (features must exist)."""
    a = {}
    for col in _ENGINE_COLS:
        a[col] = df[col].to_numpy(dtype='float64')
    regime = a['f_liquidity_regime']
    atr = a['f_atr_20']
    bar_in_day = a['bar_in_day']
    # Data-only guard component (independent of parameters): precomputed once.
    base_ok = (
        (regime != 2)
        & (bar_in_day != 0)
        & (bar_in_day < 75)
        & (atr >= 1.0)
        & ~np.isnan(a['f_depletion_ma_5'])
        & ~np.isnan(a['f_toxicity_ma_5'])
        & ~np.isnan(a['f_momentum_3'])
    )
    a['base_ok'] = base_ok
    a['adep5'] = np.abs(a['f_depletion_ma_5'])
    a['atox5'] = np.abs(a['f_toxicity_ma_5'])
    return a


def compute_position_size(df: pd.DataFrame, idx: int, base_size: int = 1) -> int:
    """Position size in contracts (Section 4.2). round(scale), clipped to [1, 2]."""
    scale = df.iloc[idx]['f_position_scale']
    return int(max(1, min(2, round(base_size * scale))))


def apply_slippage(price: float, direction: str, side: str) -> float:
    """Apply 1-tick adverse slippage per side (Section 4.3)."""
    s = _TICK
    if direction == 'long' and side == 'entry':
        return price + s
    if direction == 'long' and side == 'exit':
        return price - s
    if direction == 'short' and side == 'entry':
        return price - s
    if direction == 'short' and side == 'exit':
        return price + s
    return price


def compute_exit_pnl(entry_price: float, exit_price: float, position: int,
                     num_contracts: int) -> float:
    """Realized net P&L (gross minus $30 round-turn cost)."""
    if position == 1:
        point_pnl = exit_price - entry_price
    elif position == -1:
        point_pnl = entry_price - exit_price
    else:
        return 0.0
    gross = point_pnl * _PV * num_contracts
    return gross - _COST


def _simulate(a: Dict[str, np.ndarray], params: dict):
    """
    Core bar-by-bar state machine. Returns:
      trades  : list of tuples (entry_idx, exit_idx, dir, entry_px, exit_px,
                 entry_regime, ncon, gross, net, bars_held, reason_code, mae, mfe)
      equity  : per-bar equity array (starting $100k, includes unrealized)
      realized, position, unrealized : per-bar arrays
    """
    close = a['close']; high = a['high']; low = a['low']
    bar_in_day = a['bar_in_day']; atr = a['f_atr_20']; regime = a['f_liquidity_regime']
    dep5 = a['f_depletion_ma_5']; mom3 = a['f_momentum_3']; ema_diff = a['f_ema_diff']
    dep_diff = a['f_depletion_diff']; bar_range = a['f_bar_range']; atr_pct = a['f_atr_20_pct']
    vol_ratio = a['f_volume_ratio']; pos_scale = a['f_position_scale']
    vol_pctile = a['tmp_vol_pctile_100']; base_ok = a['base_ok']
    adep5 = a['adep5']; atox5 = a['atox5']

    p_dep = params['dep_threshold']; p_tox = params['tox_threshold']
    p_mom = params['momentum_confirm']; p_bt = params['breakthrough_threshold']
    p_exit = params['exit_bars']; p_pt = params['profit_target_pct']
    p_sl = params['stop_loss_pct']; p_minvol = params['min_volume_pctile'] / 100.0

    n = len(close)
    realized = np.zeros(n); unreal = np.zeros(n); position = np.zeros(n, dtype=np.int8)
    equity = np.empty(n)
    trades = []

    in_pos = False; pdir = 0; e_idx = -1; e_price = 0.0; e_regime = -1
    ncon = 0; mae = 0.0; mfe = 0.0; cum = 0.0

    for i in range(n):
        if not in_pos:
            d = 0
            if base_ok[i] and adep5[i] >= p_dep and atox5[i] >= p_tox and vol_pctile[i] >= p_minvol:
                r = regime[i]
                if r == 0:  # Tight-Deep: continuation
                    if dep5[i] > 0 and mom3[i] > p_mom and ema_diff[i] > 0:
                        d = 1
                    elif dep5[i] < 0 and mom3[i] < -p_mom and ema_diff[i] < 0:
                        d = -1
                elif r == 1:  # Wide-Thin: breakthrough
                    if dep_diff[i] > p_bt and bar_range[i] > atr_pct[i] * 1.2 and vol_ratio[i] > 1.5:
                        d = 1
                    elif dep_diff[i] < -p_bt and bar_range[i] > atr_pct[i] * 1.2 and vol_ratio[i] > 1.5:
                        d = -1
            if d != 0:
                in_pos = True; pdir = d; e_idx = i; e_regime = int(regime[i])
                ncon = int(max(1, min(2, round(pos_scale[i]))))
                raw = close[i]
                e_price = raw + _TICK if d == 1 else raw - _TICK
                mae = 0.0; mfe = 0.0
                position[i] = d
        else:
            reason = 0
            sl_dist = p_sl * atr[e_idx]; pt_dist = p_pt * atr[e_idx]
            if pdir == 1:
                if low[i] <= e_price - sl_dist:
                    reason = 1
                elif close[i] >= e_price + pt_dist:
                    reason = 2
            else:
                if high[i] >= e_price + sl_dist:
                    reason = 1
                elif close[i] <= e_price - pt_dist:
                    reason = 2
            if reason == 0:
                if bar_in_day[i] >= 76:
                    reason = 3
                elif (i - e_idx) >= p_exit:
                    reason = 4
                elif regime[i] == 2:
                    reason = 5

            if reason != 0:
                raw = close[i]
                x_price = raw - _TICK if pdir == 1 else raw + _TICK
                point = (x_price - e_price) if pdir == 1 else (e_price - x_price)
                gross = point * _PV * ncon
                net = gross - _COST
                cum += net
                realized[i] = net
                trades.append((e_idx, i, pdir, e_price, x_price, e_regime, ncon,
                               gross, net, i - e_idx, reason, mae, mfe))
                position[i] = 0
                in_pos = False; pdir = 0; e_idx = -1; e_price = 0.0; e_regime = -1; ncon = 0
            else:
                cp = close[i]
                point = cp - e_price if pdir == 1 else e_price - cp
                if point > mfe:
                    mfe = point
                if point < mae:
                    mae = point
                unreal[i] = point * _PV * ncon
                position[i] = pdir
        equity[i] = STARTING_EQUITY + cum + unreal[i]

    return trades, equity, realized, position, unreal


def run_backtest(df: pd.DataFrame, params: dict) -> Tuple[pd.DataFrame, List[Trade]]:
    """Full backtest: returns DataFrame with P&L/equity columns and a list of Trades."""
    df = df.copy()
    a = extract_arrays(df)
    rec, equity, realized, position, unreal = _simulate(a, params)

    ts = df['ts_event'].to_numpy()
    trades: List[Trade] = []
    for (ei, xi, d, ep, xp, er, nc, gross, net, bh, rc, mae, mfe) in rec:
        trades.append(Trade(
            entry_idx=ei, exit_idx=xi,
            entry_time=df['ts_event'].iloc[ei], exit_time=df['ts_event'].iloc[xi],
            direction=d, entry_price=ep, exit_price=xp, entry_regime=er,
            num_contracts=nc, gross_pnl=gross, net_pnl=net, bars_held=bh,
            exit_reason=EXIT_REASON_LABELS[rc],
            max_adverse_excursion=mae, max_favorable_excursion=mfe,
        ))

    df['position'] = position
    df['realized_pnl'] = realized
    df['unrealized_pnl'] = unreal
    df['cumulative_pnl'] = np.cumsum(realized) + unreal
    df['equity'] = equity
    return df, trades


def compute_trade_statistics(trades: List[Trade], df: pd.DataFrame) -> dict:
    """Comprehensive trade statistics (Section 4.5)."""
    if not trades:
        return {'error': 'No trades generated', 'total_trades': 0, 'win_rate': 0,
                'trades_per_day': 0, 'total_net_pnl': 0.0}
    stats = {}
    net_pnls = np.array([t.net_pnl for t in trades])
    stats['total_trades'] = len(trades)
    stats['long_trades'] = sum(1 for t in trades if t.direction == 1)
    stats['short_trades'] = sum(1 for t in trades if t.direction == -1)
    stats['total_net_pnl'] = float(net_pnls.sum())
    stats['total_gross_pnl'] = float(sum(t.gross_pnl for t in trades))
    stats['total_costs'] = stats['total_gross_pnl'] - stats['total_net_pnl']
    stats['avg_pnl_per_trade'] = float(net_pnls.mean())
    stats['pnl_std'] = float(net_pnls.std())
    stats['median_pnl'] = float(np.median(net_pnls))

    wins = [t for t in trades if t.net_pnl > 0]
    losses = [t for t in trades if t.net_pnl <= 0]
    stats['winning_trades'] = len(wins)
    stats['losing_trades'] = len(losses)
    stats['win_rate'] = len(wins) / len(trades)
    stats['avg_win'] = float(np.mean([t.net_pnl for t in wins])) if wins else 0.0
    stats['avg_loss'] = float(np.mean([t.net_pnl for t in losses])) if losses else 0.0
    loss_sum = sum(t.net_pnl for t in losses)
    stats['profit_factor'] = (sum(t.net_pnl for t in wins) / abs(loss_sum)) if loss_sum != 0 else float('inf')
    stats['payoff_ratio'] = abs(stats['avg_win'] / stats['avg_loss']) if stats['avg_loss'] != 0 else float('inf')

    stats['avg_bars_held'] = float(np.mean([t.bars_held for t in trades]))
    stats['median_bars_held'] = float(np.median([t.bars_held for t in trades]))

    exit_reasons = {}
    for t in trades:
        exit_reasons[t.exit_reason] = exit_reasons.get(t.exit_reason, 0) + 1
    stats['exit_reasons'] = exit_reasons

    for regime, name in [(0, 'tight_deep'), (1, 'wide_thin')]:
        rt = [t for t in trades if t.entry_regime == regime]
        if rt:
            rw = [t for t in rt if t.net_pnl > 0]
            stats[f'{name}_accuracy'] = len(rw) / len(rt)
            stats[f'{name}_trades'] = len(rt)
            stats[f'{name}_avg_pnl'] = float(np.mean([t.net_pnl for t in rt]))
        else:
            stats[f'{name}_accuracy'] = 0
            stats[f'{name}_trades'] = 0
            stats[f'{name}_avg_pnl'] = 0
    stats['disrupted_trades'] = sum(1 for t in trades if t.entry_regime == 2)

    stats['avg_mae'] = float(np.mean([t.max_adverse_excursion for t in trades]))
    stats['avg_mfe'] = float(np.mean([t.max_favorable_excursion for t in trades]))

    trading_days = df['date'].nunique()
    stats['trades_per_day'] = stats['total_trades'] / trading_days if trading_days > 0 else 0
    return stats


def compute_equity_metrics(df: pd.DataFrame, trades: List[Trade]) -> dict:
    """Equity-curve metrics: drawdown, Sharpe, Sortino, Calmar (Section 4.6)."""
    metrics = {}
    equity = df['equity'].values
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    drawdown_dollars = equity - peak

    metrics['final_equity'] = float(equity[-1])
    metrics['total_return_pct'] = float((equity[-1] / equity[0] - 1) * 100)
    metrics['max_drawdown_pct'] = float(drawdown.min() * 100)
    metrics['max_drawdown_dollars'] = float(drawdown_dollars.min())

    max_dd_idx = int(np.argmin(drawdown))
    peak_before = int(equity[:max_dd_idx + 1].argmax())
    metrics['max_drawdown_duration_bars'] = max_dd_idx - peak_before

    returns = pd.Series(equity).pct_change().dropna()
    if len(returns) > 1 and returns.std() > 0:
        metrics['sharpe_ratio'] = float((returns.mean() / returns.std()) * np.sqrt(ANNUALIZATION))
    else:
        metrics['sharpe_ratio'] = 0.0

    downside = returns[returns < 0]
    if len(downside) > 0 and downside.std() > 0:
        metrics['sortino_ratio'] = float((returns.mean() / downside.std()) * np.sqrt(ANNUALIZATION))
    else:
        metrics['sortino_ratio'] = 0.0

    if abs(metrics['max_drawdown_pct']) > 0:
        metrics['calmar_ratio'] = metrics['total_return_pct'] / abs(metrics['max_drawdown_pct'])
    else:
        metrics['calmar_ratio'] = float('inf')

    df['peak_equity'] = peak
    df['drawdown_pct'] = drawdown * 100
    df['drawdown_dollars'] = drawdown_dollars
    return metrics


def fast_metrics(a: Dict[str, np.ndarray], params: dict, trading_days: int) -> Tuple[dict, dict]:
    """Lightweight evaluation used inside optimization loops (no DataFrame/Trade objects)."""
    rec, equity, realized, position, unreal = _simulate(a, params)
    n_tr = len(rec)
    if n_tr == 0:
        return ({'total_trades': 0, 'win_rate': 0.0, 'trades_per_day': 0.0,
                 'wide_thin_accuracy': 0.0, 'tight_deep_accuracy': 0.0,
                 'total_net_pnl': 0.0, 'profit_factor': 0.0},
                {'sharpe_ratio': 0.0, 'max_drawdown_pct': 0.0})

    net = np.array([r[8] for r in rec])
    regimes = np.array([r[5] for r in rec])
    wins = net > 0
    wr = wins.mean()
    wt = regimes == 1
    td = regimes == 0
    wt_acc = (net[wt] > 0).mean() if wt.any() else 0.0
    td_acc = (net[td] > 0).mean() if td.any() else 0.0
    win_sum = net[wins].sum()
    loss_sum = net[~wins].sum()
    pf = (win_sum / abs(loss_sum)) if loss_sum != 0 else float('inf')

    peak = np.maximum.accumulate(equity)
    dd = ((equity - peak) / peak).min() * 100
    rets = pd.Series(equity).pct_change().dropna()
    sharpe = float((rets.mean() / rets.std()) * np.sqrt(ANNUALIZATION)) if rets.std() > 0 else 0.0

    stats = {'total_trades': n_tr, 'win_rate': float(wr),
             'trades_per_day': n_tr / trading_days if trading_days else 0.0,
             'wide_thin_accuracy': float(wt_acc), 'tight_deep_accuracy': float(td_acc),
             'total_net_pnl': float(net.sum()), 'profit_factor': float(pf)}
    equity_m = {'sharpe_ratio': sharpe, 'max_drawdown_pct': float(dd)}
    return stats, equity_m
