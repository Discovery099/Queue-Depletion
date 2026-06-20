"""
ML PROTOTYPE (research) — does the 45-feature set carry any predictive signal?

A strictly anti-curve-fit experiment (Section 8 / 5.5 compliant):
  * Strong-L2 logistic regression on a FIXED curated feature subset (low capacity).
  * Label = sign of the H-bar forward return (H fixed = 3).
  * PURGED walk-forward on the development set (H-bar embargo prevents label leakage
    across the IS/OOS boundary).
  * Hyperparameters fixed BEFORE the test set is touched: {H, C, feature_set,
    prob_margin}. The probability margin is set a-priori (0.05), not tuned to OOS PnL.
  * Test set used EXACTLY ONCE for final evaluation. No model selection on it.
  * Features standardized with a scaler fit on TRAIN ONLY (no leakage).
  * Costs ($30/round turn) + 1-tick/side slippage included. No overnight positions
    (exit capped at the day's end). Reproducible (seed=42).
  * Binomial significance test on the out-of-sample win rate.

Run: python -m strategy_02_queue_depletion.ml_prototype
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from scipy import stats as scipy_stats

from strategy_02_queue_depletion.config import (
    OUTPUT_DIR, RANDOM_SEED, ES_POINT_VALUE, ES_TICK_SIZE, TRANSACTION_COST_PER_TRADE,
)
from strategy_02_queue_depletion.data_pipeline import load_data, split_data
from strategy_02_queue_depletion.features import compute_all_features
from strategy_02_queue_depletion.validation import generate_wfa_windows

# ---- FIXED HYPERPARAMETERS (declared before any test-set contact) -------------------
H = 3                 # forward horizon (bars) — matches the strategy's holding period
C = 0.05              # inverse L2 strength (strong regularization -> low capacity)
PROB_MARGIN = 0.05    # only trade when |p_up - 0.5| >= margin (a-priori confidence band)
FEATURES = [
    'f_returns', 'f_log_returns', 'f_bar_range', 'f_body_size', 'f_body_direction',
    'f_upper_shadow', 'f_lower_shadow', 'f_bvc_ratio', 'f_bvc_imbalance',
    'f_atr_20_pct', 'f_vol_realized_20', 'f_vol_ratio', 'f_volume_ratio', 'f_volume_zscore_20',
    'f_depletion_raw', 'f_depletion_ma_5', 'f_depletion_ma_10', 'f_depletion_diff',
    'f_toxicity_raw', 'f_toxicity_ma_5', 'f_toxicity_zscore',
    'f_ema_diff', 'f_price_vs_ema20', 'f_momentum_3', 'f_momentum_6',
    'f_liquidity_score', 'f_regime_tight_deep', 'f_regime_wide_thin',
]


def _prepare(df_feat: pd.DataFrame):
    """Return arrays: X, label y, tradable mask, exit index, close."""
    df = df_feat.reset_index(drop=True)
    n = len(df)
    close = df['close'].to_numpy()
    bar_in_day = df['bar_in_day'].to_numpy()
    regime = df['f_liquidity_regime'].to_numpy()
    atr = df['f_atr_20'].to_numpy()

    # Exit index: H bars ahead, capped at the last bar of the same trading day (no overnight)
    day_codes = pd.factorize(df['date'])[0]
    day_end = np.empty(n, dtype=int)
    last = n - 1
    for i in range(n - 1, -1, -1):
        if i == n - 1 or day_codes[i] != day_codes[i + 1]:
            last = i
        day_end[i] = last
    exit_idx = np.minimum(np.arange(n) + H, day_end)

    X = df[FEATURES].to_numpy(dtype='float64')
    finite = np.isfinite(X).all(axis=1)

    fwd_ret = close[exit_idx] - close
    y = (fwd_ret > 0).astype(int)

    tradable = (
        (regime != 2) & (bar_in_day >= 1) & (bar_in_day <= 74) & (atr >= 1.0)
        & finite & (exit_idx > np.arange(n))
    )
    return X, y, tradable, exit_idx, close


def _trade_pnl(close, idxs, dirs, exit_idx):
    """Cost- and slippage-aware net P&L per selected trade (qty=1)."""
    ep = close[idxs]
    xp = close[exit_idx[idxs]]
    gross = dirs * (xp - ep) * ES_POINT_VALUE          # slippage + commission bundled in COST
    net = gross - TRANSACTION_COST_PER_TRADE
    return net


def _eval_block(close, exit_idx, idxs, proba_up):
    """Given candidate bar indices and P(up), apply margin filter and compute metrics."""
    conf = np.abs(proba_up - 0.5) >= PROB_MARGIN
    sel = idxs[conf]
    if len(sel) == 0:
        return {'trades': 0, 'accuracy': 0.0, 'win_rate': 0.0, 'net_pnl': 0.0,
                'profit_factor': 0.0, 'avg_pnl': 0.0}, sel, np.array([])
    dirs = np.where(proba_up[conf] >= 0.5, 1, -1)
    net = _trade_pnl(close, sel, dirs, exit_idx)
    wins = net > 0
    win_sum = net[wins].sum(); loss_sum = net[~wins].sum()
    pf = (win_sum / abs(loss_sum)) if loss_sum != 0 else float('inf')
    # directional accuracy (ignoring costs): predicted dir matches realized fwd dir
    realized_dir = np.sign(close[exit_idx[sel]] - close[sel])
    acc = float(np.mean(dirs == realized_dir))
    return ({'trades': int(len(sel)), 'accuracy': round(acc, 4),
             'win_rate': round(float(wins.mean()), 4), 'net_pnl': round(float(net.sum()), 0),
             'profit_factor': round(float(pf), 3), 'avg_pnl': round(float(net.mean()), 2)},
            sel, net)


def purged_walk_forward(df_dev_feat):
    """Purged WFA on dev: train LR on IS (embargo H bars), evaluate OOS. Aggregated."""
    X, y, tradable, exit_idx, close = _prepare(df_dev_feat)
    windows = generate_wfa_windows()
    all_sel, all_net, fold_accs = [], [], []
    for (is_start, is_end, oos_start, oos_end) in windows:
        # Embargo: drop last H bars of IS so no training label peeks into OOS
        tr_mask = np.zeros(len(X), dtype=bool)
        tr_mask[is_start:is_end - H] = True
        tr_mask &= tradable
        te_mask = np.zeros(len(X), dtype=bool)
        te_mask[oos_start:oos_end] = True
        te_mask &= tradable
        if tr_mask.sum() < 500 or te_mask.sum() < 50:
            continue
        clf = make_pipeline(StandardScaler(),
                            LogisticRegression(C=C, max_iter=1000, random_state=RANDOM_SEED))
        clf.fit(X[tr_mask], y[tr_mask])
        te_idx = np.where(te_mask)[0]
        proba = clf.predict_proba(X[te_idx])[:, 1]
        m, sel, net = _eval_block(close, exit_idx, te_idx, proba)
        if m['trades'] > 0:
            fold_accs.append(m['accuracy'])
            all_sel.append(sel); all_net.append(net)
    sel = np.concatenate(all_sel) if all_sel else np.array([], dtype=int)
    net = np.concatenate(all_net) if all_net else np.array([])
    return sel, net, fold_accs, close, exit_idx


def _agg(net):
    if len(net) == 0:
        return {'trades': 0, 'win_rate': 0.0, 'net_pnl': 0.0, 'profit_factor': 0.0}
    wins = net > 0
    ws, ls = net[wins].sum(), net[~wins].sum()
    pf = (ws / abs(ls)) if ls != 0 else float('inf')
    return {'trades': int(len(net)), 'win_rate': round(float(wins.mean()), 4),
            'net_pnl': round(float(net.sum()), 0), 'profit_factor': round(float(pf), 3)}


def run():
    np.random.seed(RANDOM_SEED)
    print("=" * 88)
    print("STRAT-02 ML PROTOTYPE — anti-curve-fit feature predictivity test")
    print(f"Fixed hyperparameters: H={H}, C={C}, prob_margin={PROB_MARGIN}, "
          f"n_features={len(FEATURES)}")
    print("=" * 88)

    df = load_data()
    df_dev, df_test = split_data(df)
    df_dev_feat = compute_all_features(df_dev)
    df_test_feat = compute_all_features(df_test)
    dev_days = df_dev['date'].nunique()
    test_days = df_test['date'].nunique()

    # ---- Development: PURGED walk-forward OOS (no test contact) ----------------------
    sel, net, fold_accs, _, _ = purged_walk_forward(df_dev_feat)
    dev_oos = _agg(net)
    dev_oos['trades_per_day'] = round(dev_oos['trades'] / dev_days, 2)
    dev_oos['mean_fold_accuracy'] = round(float(np.mean(fold_accs)), 4) if fold_accs else 0.0
    print("\n[DEV purged-WFA OOS]")
    print(f"  folds_evaluated={len(fold_accs)}  trades={dev_oos['trades']} "
          f"({dev_oos['trades_per_day']}/day)  win_rate={dev_oos['win_rate']*100:.2f}%  "
          f"mean_fold_dir_acc={dev_oos['mean_fold_accuracy']*100:.2f}%  "
          f"PF={dev_oos['profit_factor']}  net=${dev_oos['net_pnl']:,.0f}")

    # ---- FINAL: train on ALL dev, evaluate TEST exactly once -------------------------
    Xd, yd, trd, exd, cld = _prepare(df_dev_feat)
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(C=C, max_iter=1000, random_state=RANDOM_SEED))
    clf.fit(Xd[trd], yd[trd])

    Xt, yt, trt, ext, clt = _prepare(df_test_feat)
    te_idx = np.where(trt)[0]
    proba = clf.predict_proba(Xt[te_idx])[:, 1]
    test_m, test_sel, test_net = _eval_block(clt, ext, te_idx, proba)
    test_m['trades_per_day'] = round(test_m['trades'] / test_days, 2)

    # Binomial significance on test win rate
    wins = int((test_net > 0).sum()); ntr = int(len(test_net))
    binom_p = scipy_stats.binomtest(wins, ntr, 0.5, alternative='greater').pvalue if ntr > 0 else 1.0
    test_m['binomial_p_value'] = round(float(binom_p), 6)
    overfit_gap = round(dev_oos['win_rate'] - test_m['win_rate'], 4)

    print("\n[TEST — final, run once]")
    print(f"  trades={test_m['trades']} ({test_m['trades_per_day']}/day)  "
          f"win_rate={test_m['win_rate']*100:.2f}%  dir_acc={test_m['accuracy']*100:.2f}%  "
          f"PF={test_m['profit_factor']}  net=${test_m['net_pnl']:,.0f}  "
          f"binomial_p={test_m['binomial_p_value']}")
    print(f"  overfit gap (dev_oos_wr - test_wr) = {overfit_gap*100:.2f} pts")

    verdict = ("FEATURES CARRY A WEAK EDGE" if (test_m['win_rate'] > 0.52 and
               test_m['binomial_p_value'] < 0.05 and test_m['net_pnl'] > 0)
               else "NO EXPLOITABLE EDGE in the feature set under these constraints")
    print(f"\n  VERDICT: {verdict}")

    out = {'hyperparameters': {'H': H, 'C': C, 'prob_margin': PROB_MARGIN,
                               'n_features': len(FEATURES), 'features': FEATURES},
           'dev_oos_purged_wfa': dev_oos, 'test_once': test_m,
           'overfit_gap_winrate': overfit_gap, 'verdict': verdict,
           'anti_curve_fit': {
               'purged_walk_forward_embargo_bars': H,
               'test_set_uses': 1, 'hyperparameters_fixed_before_test': True,
               'scaler_fit_on_train_only': True, 'costs_included_usd_per_rt': TRANSACTION_COST_PER_TRADE,
               'overnight_positions': False, 'random_seed': RANDOM_SEED,
               'trades_test': ntr, 'trades_ge_1000': ntr >= 1000}}
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "strategy_02_ml_prototype.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  Results written to {path}")
    print("=" * 88)
    return out


if __name__ == "__main__":
    run()
