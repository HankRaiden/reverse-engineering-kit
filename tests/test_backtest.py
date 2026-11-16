import numpy as np
import pandas as pd
import pytest

from rekit.backtest import BacktestConfig, run_backtest


def flat(n=40):
    """Flat market: open=close=100, high=101, low=99 -> ATR(14)=2 exactly."""
    idx = pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC", name="ts")
    return pd.DataFrame({"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 1.0}, index=idx)


def sig_at(df, i, side=1):
    s = pd.Series(0, index=df.index)
    s.iloc[i] = side
    return s


CFG = BacktestConfig(risk_pct=1.0, fee_bps=5.5, slippage_bps=2.0, stop_atr=1.5, target_r=2.0)


def costs_r(entry, dist, cfg=CFG):
    return 2 * cfg.fee_bps / 1e4 * entry / dist


def test_entry_next_bar_open():
    df = flat()
    df.iloc[21, 0] = 100.5  # distinctive open on the bar after the signal
    df.iloc[21, 1] = 101.0
    res = run_backtest(df, sig_at(df, 20), CFG)
    t = res.trades.iloc[0]
    assert t.entry_ts == df.index[21]
    assert t.entry == pytest.approx(100.5 * (1 + 2.0 / 1e4))


def test_stop_first_when_both_hit():
    df = flat()
    df.iloc[22, df.columns.get_loc("high")] = 110.0
    df.iloc[22, df.columns.get_loc("low")] = 90.0
    res = run_backtest(df, sig_at(df, 20), CFG)
    t = res.trades.iloc[0]
    assert t.exit_reason == "stop"
    entry, dist = 100 * 1.0002, 3.0
    expected = (t.stop * (1 - 2.0 / 1e4) - entry) / dist - costs_r(entry, dist)
    assert t.r_multiple == pytest.approx(expected)
    assert -1.05 < t.r_multiple < -1.0


def test_target_hit_gives_target_r():
    df = flat()
    df.iloc[23, df.columns.get_loc("high")] = 107.0
    res = run_backtest(df, sig_at(df, 20), CFG)
    t = res.trades.iloc[0]
    assert t.exit_reason == "target"
    entry, dist = 100 * 1.0002, 3.0
    assert t.r_multiple == pytest.approx(2.0 - costs_r(entry, dist))


def test_short_target():
    df = flat()
    df.iloc[23, df.columns.get_loc("low")] = 93.0
    res = run_backtest(df, sig_at(df, 20, side=-1), CFG)
    t = res.trades.iloc[0]
    assert (t.side, t.exit_reason) == (-1, "target")
    assert t.r_multiple > 1.9


def test_one_position_at_a_time():
    df = flat(60)
    s = pd.Series(1, index=df.index)
    res = run_backtest(df, s, CFG)
    tr = res.trades
    assert (tr.entry_ts.iloc[1:].to_numpy() > tr.exit_ts.iloc[:-1].to_numpy()).all()


def test_time_exit_and_end_exit():
    df = flat()
    res = run_backtest(df, sig_at(df, 20), BacktestConfig(max_bars=3))
    assert res.trades.iloc[0].exit_reason == "time"
    res2 = run_backtest(df, sig_at(df, 20), CFG)
    assert res2.trades.iloc[0].exit_reason == "end"


def test_return_pct_is_risk_scaled(ohlcv):
    s = np.sign(ohlcv.close.diff(5)).fillna(0).astype(int)
    res = run_backtest(ohlcv, s, BacktestConfig(risk_pct=0.5))
    np.testing.assert_allclose(res.trades.return_pct, res.trades.r_multiple * 0.5)


def test_equity_compounds(ohlcv):
    s = np.sign(ohlcv.close.diff(5)).fillna(0).astype(int)
    res = run_backtest(ohlcv, s, CFG)
    assert len(res.trades) > 5
    assert res.equity.iloc[0] == 1.0 or res.equity.index[0] == ohlcv.index[0]
    assert res.equity.iloc[-1] == pytest.approx(np.prod(1 + res.trades.return_pct / 100))


def test_gap_through_stop_fills_at_open():
    df = flat()
    df.iloc[23, :4] = [95.0, 95.5, 94.0, 95.0]  # opens below the stop
    res = run_backtest(df, sig_at(df, 20), CFG)
    t = res.trades.iloc[0]
    assert t.exit_reason == "stop"
    assert t.exit == pytest.approx(95.0 * (1 - 2.0 / 1e4))


def test_no_currency_in_output(ohlcv):
    res = run_backtest(ohlcv, pd.Series(1, index=ohlcv.index), CFG)
    assert not any(k in c.lower() for c in res.trades.columns for k in ("usd", "eur"))
