"""Performance metrics. Everything in R or percent."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .backtest import BacktestResult


def max_drawdown_pct(equity: pd.Series) -> float:
    """Deepest fall below a previous high, in percent (negative number)."""
    if len(equity) == 0:
        return 0.0
    eq = pd.Series(equity, dtype=float)
    return float(((eq / eq.cummax()) - 1).min() * 100)


def sharpe_annual(equity: pd.Series, periods_per_year: int = 365) -> float:
    """Annualised Sharpe of daily account returns (crypto trades every day)."""
    if len(equity) < 3 or not isinstance(equity.index, pd.DatetimeIndex):
        return float("nan")
    daily = equity.resample("1D").last().ffill().pct_change().dropna()
    sd = daily.std()
    return float(daily.mean() / sd * np.sqrt(periods_per_year)) if sd > 0 else float("nan")


def summarize(result: BacktestResult) -> dict:
    r = result.trades["r_multiple"].to_numpy(dtype=float) if len(result.trades) else np.array([])
    wins, losses = r[r > 0].sum(), -r[r < 0].sum()
    n = len(r)
    return {
        "n_trades": n,
        "hit_rate": float((r > 0).mean()) if n else float("nan"),
        "profit_factor": float(wins / losses) if losses > 0 else float("nan"),
        "expectancy_r": float(r.mean()) if n else float("nan"),
        "total_return_pct": float((result.equity.iloc[-1] - 1) * 100) if len(result.equity) else 0.0,
        "max_drawdown_pct": max_drawdown_pct(result.equity),
        "sharpe_annual": sharpe_annual(result.equity),
    }
