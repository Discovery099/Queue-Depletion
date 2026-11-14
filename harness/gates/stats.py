"""Statistical corrections for the number of trials (SPEC 12.3, 12.4, 12.5, 12.7, 12.11)."""
import math

import numpy as np
from scipy import stats as ss


def expected_max_sharpe(n_trials, var_sr):
    """Expected maximum of n zero-skill Sharpe ratios with cross-trial variance var_sr."""
    n = max(2.0, float(n_trials))
    g = 0.5772156649
    return math.sqrt(max(var_sr, 1e-12)) * ((1 - g) * ss.norm.ppf(1 - 1.0 / n) + g * ss.norm.ppf(1 - 1.0 / (n * math.e)))


def deflated_sharpe(daily, n_trials, var_sr):
    """Probability that the true per-session Sharpe exceeds the expected maximum of n zero-skill trials,
    adjusted for sample length, skewness and kurtosis (deflated Sharpe ratio)."""
    x = np.asarray(daily, float)
    t = len(x)
    sd = x.std(ddof=1)
    if t < 30 or sd <= 0:
        return 0.0, 0.0, 0.0
    sr = x.mean() / sd
    z = (x - x.mean()) / sd
    g3, g4 = float((z ** 3).mean()), float((z ** 4).mean())
    sr0 = expected_max_sharpe(n_trials, var_sr)
    den = math.sqrt(max(1e-12, 1 - g3 * sr + (g4 - 1) / 4.0 * sr * sr))
    return float(ss.norm.cdf((sr - sr0) * math.sqrt(t - 1) / den)), float(sr), float(sr0)


def pbo_cscv(perf, n_blocks=16, n_combos=2000, seed=0):
    """Probability of backtest overfitting by combinatorially symmetric cross-validation.

    perf: array (configs, blocks) of per-block performance.  For each choice of half the blocks as
    in-sample, the best in-sample config's rank out-of-sample is recorded; PBO is the share of
    choices where it lands below the out-of-sample median.  Also returns the slope of out-of-sample
    on in-sample performance across configs (a negative slope fails)."""
    perf = np.asarray(perf, float)
    n_cfg, nb = perf.shape
    if n_cfg < 4:
        return {"pbo": None, "slope": None, "configs": n_cfg, "note": "fewer than 4 configurations"}
    rng = np.random.default_rng(seed)
    half = nb // 2
    below, slopes = 0, []
    for _ in range(n_combos):
        idx = rng.permutation(nb)
        a, b = perf[:, idx[:half]].mean(1), perf[:, idx[half:]].mean(1)
        best = int(np.argmax(a))
        rank = (b < b[best]).sum() / (n_cfg - 1.0)          # 1 = best out of sample
        below += rank < 0.5
        if a.std() > 0:
            slopes.append(np.polyfit(a, b, 1)[0])
    return {"pbo": below / n_combos, "slope": float(np.mean(slopes)) if slopes else 0.0, "configs": n_cfg, "combos": n_combos}


def block_bootstrap(net, tick_value, block=10, n=5000, seed=0):
    """Resample trades in blocks with replacement; 5th percentiles of profit factor and win rate, 95th of drawdown."""
    net = np.asarray(net, float)
    tv = np.broadcast_to(np.asarray(tick_value, float), net.shape)
    m = len(net)
    if m < 2 * block:
        return {"pf_p5": 0.0, "wr_p5": 0.0, "dd_p95": 0.0, "n": m}
    rng = np.random.default_rng(seed)
    nblk = int(math.ceil(m / block))
    starts = rng.integers(0, m - block + 1, (n, nblk))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n, -1)[:, :m]
    x = net[idx]
    w = x > tv[idx]
    gp = np.where(w, x, 0).sum(1)
    gl = -np.where(~w, x, 0).sum(1)
    pf = np.where(gl > 0, gp / np.maximum(gl, 1e-9), 99.0)
    cum = np.cumsum(x, axis=1)
    dd = (np.maximum.accumulate(np.maximum(cum, 0), axis=1) - cum).max(1)
    return {"pf_p5": float(np.percentile(pf, 5)), "wr_p5": float(np.percentile(w.mean(1), 5)), "dd_p95": float(np.percentile(dd, 95)),
            "net_p5": float(np.percentile(x.sum(1), 5)), "n": m}


def reality_check(candidate_daily, benchmark_daily, others_daily, n=2000, seed=0, mean_block=10):
    """White's reality check with the stationary bootstrap: p-value that the best of the family
    (candidate and the other clustered trials) beats the benchmark by luck."""
    c = np.asarray(candidate_daily, float) - np.asarray(benchmark_daily, float)
    fam = [c] + [np.asarray(o, float) - np.asarray(benchmark_daily, float) for o in others_daily]
    f = np.vstack(fam)
    t = f.shape[1]
    stat = math.sqrt(t) * f.mean(1).max()
    rng = np.random.default_rng(seed)
    cnt = 0
    p = 1.0 / mean_block
    for _ in range(n):
        idx = np.empty(t, np.int64)
        idx[0] = rng.integers(t)
        jump = rng.random(t) < p
        new = rng.integers(0, t, t)
        for i in range(1, t):
            idx[i] = new[i] if jump[i] else (idx[i - 1] + 1) % t
        b = f[:, idx].mean(1) - f.mean(1)
        cnt += math.sqrt(t) * b.max() >= stat
    return cnt / n


def benjamini_hochberg(pvals, q=0.10):
    """Indices accepted by the false-discovery-rate procedure at level q."""
    p = np.asarray(pvals, float)
    if len(p) == 0:
        return []
    order = np.argsort(p)
    thr = q * (np.arange(len(p)) + 1) / len(p)
    ok = np.flatnonzero(p[order] <= thr)
    return sorted(order[: ok.max() + 1].tolist()) if len(ok) else []


def effective_trials(series, max_sample=1500, seed=0):
    """Effective number of independent trials (SPEC 12.3): cluster the trials' out-of-sample daily return
    series by correlation distance and take the number of clusters with the best silhouette.

    Returns {'raw', 'n_eff', 'var_sharpe'}.  `series` is an array (trials, sessions)."""
    from scipy.cluster.hierarchy import fcluster, linkage
    from sklearn.metrics import silhouette_score
    x = np.asarray(series, float)
    raw = len(x)
    keep = x.std(1) > 0
    x = x[keep]
    if len(x) < 10:
        return {"raw": raw, "n_eff": max(1, len(x)), "var_sharpe": 0.0, "sampled": len(x)}
    rng = np.random.default_rng(seed)
    if len(x) > max_sample:
        x = x[rng.choice(len(x), max_sample, replace=False)]
    sr = x.mean(1) / x.std(1)
    c = np.corrcoef(x)
    d = np.sqrt(np.clip(0.5 * (1 - c), 0, 1))
    np.fill_diagonal(d, 0.0)
    z = linkage(d[np.triu_indices(len(x), 1)], method="average")
    best_k, best_s = 2, -1.0
    for k in sorted({max(2, int(len(x) * f)) for f in (0.02, 0.05, 0.1, 0.2, 0.3, 0.45, 0.6)}):
        lab = fcluster(z, k, criterion="maxclust")
        if len(set(lab)) < 2:
            continue
        s = silhouette_score(d, lab, metric="precomputed")
        if s > best_s:
            best_k, best_s = len(set(lab)), s
    scale = raw / len(x) if raw > len(x) else 1.0
    lab = fcluster(z, best_k, criterion="maxclust")
    csr = np.array([sr[lab == k].mean() for k in np.unique(lab)])
    return {"raw": raw, "n_eff": int(math.ceil(best_k * scale)), "clusters_in_sample": int(best_k), "silhouette": float(best_s),
            "var_sharpe": float(csr.var()), "sampled": len(x)}
