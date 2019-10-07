from datetime import datetime
from typing import List, Tuple

from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
from vnpy.trader.constant import Interval


class StrategyOptimizer:

    def __init__(self, timeframe: Interval, from_date: datetime, to_date: datetime,
                 execution_fee: float = 0, slippage: float = 0, size: int = 1, capital: int = 1_000_000_000,
                 min_price_tick: float = 0.0001):
        self._tf = timeframe
        self._from_date = from_date
        self._to_date = to_date
        self._fee = execution_fee
        self._slippage = slippage
        self._size = size
        self._capital = capital
        self._min_tick = min_price_tick

    def optimize_strategy(self, symbol: str, strategy, opt_params: List[Tuple], *, target_metric="sharpe_ratio",
                          alg='genetic'):
        engine = BacktestingEngine()
        engine.set_parameters(
            vt_symbol=symbol,
            interval=self._tf,
            start=self._from_date,
            end=self._to_date,
            rate=self._fee,
            slippage=self._slippage,
            size=self._size,
            pricetick=self._min_tick,
            capital=self._capital,
        )
        engine.add_strategy(strategy, {})
        setting = OptimizationSetting()
        setting.set_target(target_metric)
        for o in opt_params:
            setting.add_parameter(*o)

        if alg:
            results = engine.run_ga_optimization(setting)
        else:
            results = engine.run_optimization(setting)

        return results
