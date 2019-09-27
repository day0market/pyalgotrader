from collections import namedtuple
from datetime import datetime
from itertools import combinations
from typing import List, Union, Optional

from pandas import DataFrame

from vnpy.app.cta_strategy.backtesting import BacktestingEngine
from vnpy.trader.constant import Interval

StrategyConfig = namedtuple("StrategySetup", ("strategy_cls", "settings", "symbols"))


class BacktestRunner:

    def __init__(self, timeframe: Interval, from_date: datetime, to_date: datetime,
                 execution_fee: float = 0, slippage: float = 0, size: int = 1, capital: int = 1_000_000_000,
                 min_price_tick: float = 0.0001, show_charts=True):

        self._tf = timeframe
        self._from_date = from_date
        self._to_date = to_date
        self._fee = execution_fee
        self._slippage = slippage
        self._size = size
        self._capital = capital
        self._min_tick = min_price_tick
        self._show_charts = show_charts

    def run(self, strategies: Union[List[StrategyConfig], StrategyConfig]) -> DataFrame:
        if isinstance(strategies, List):
            assert len(strategies) > 0
            return self.__run_portfolio_bt(strategies)

        generated_strategies = self.__split_to_single_symbol_strategies(strategies)
        if generated_strategies:
            return self.__run_portfolio_bt(generated_strategies)

        elif not isinstance(strategies.symbols, str):
            raise Exception(
                f'`symbols` in strategy config should be sequence or string. '
                f'Got: {strategies.symbols} ({type(strategies.symbols)}'
            )

        return self.__run_single_symbol_bt(strategies)

    def __run_single_symbol_bt(self, strategy_config: StrategyConfig, for_portfolio=False) -> DataFrame:
        engine = BacktestingEngine()
        engine.set_parameters(
            vt_symbol=strategy_config.symbols,
            interval=self._tf,
            start=self._from_date,
            end=self._to_date,
            rate=self._fee,
            slippage=self._slippage,
            size=self._size,
            pricetick=self._min_tick,
            capital=self._capital,
        )

        engine.add_strategy(strategy_config.strategy_cls, strategy_config.settings)

        engine.load_data()
        engine.run_backtesting()
        df = engine.calculate_result()

        if not for_portfolio:
            engine.calculate_statistics()
            if self._show_charts:
                engine.show_chart()

        return df

    @staticmethod
    def __split_to_single_symbol_strategies(strategy: StrategyConfig) -> Optional[List[StrategyConfig]]:
        symbols = strategy.symbols if type(strategy.symbols) in (list, set, tuple) else [strategy.symbols]
        strategy_classes = strategy.strategy_cls if type(strategy.strategy_cls) in (list, set, tuple) \
            else [strategy.strategy_cls]

        if len(symbols) == len(strategy_classes) == 1:
            return None

        combs = combinations(symbols, strategy_classes)
        generated = []
        for symb, str_cls in combs:
            generated.append(StrategyConfig(str_cls, strategy.settings, symb))

        return generated

    def __run_portfolio_bt(self, strategies_configs: List[StrategyConfig]) -> DataFrame:
        calculated = []
        for s in strategies_configs:
            generated = self.__split_to_single_symbol_strategies(s)
            if generated:
                for g in generated:
                    df = self.__run_single_symbol_bt(g, for_portfolio=True)
                    if not df.empty:
                        calculated.append(df)
            else:
                df = self.__run_single_symbol_bt(s, for_portfolio=True)
                if not df.empty:
                    calculated.append(df)

        if not calculated:
            return DataFrame()  # better return empty DF than None

        total = sum(calculated)
        total.dropna(inplace=True)

        engine = BacktestingEngine()
        engine.calculate_statistics(total)

        if self._show_charts:
            engine.show_chart(total)

        return total
