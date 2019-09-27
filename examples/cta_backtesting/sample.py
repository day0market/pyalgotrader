from datetime import datetime

from vnpy.app.cta_strategy.strategies.xbt_strategy import XbtStrategy
from vnpy.trader.constant import Interval
from vnpy.runners.backtest_runner import BacktestRunner, StrategyConfig

if __name__ == '__main__':
    b = BacktestRunner(
        Interval.MINUTE,
        datetime(2016, 1, 1),
        datetime(2019, 9, 10),
        show_charts=True
    )
    strategy_config = StrategyConfig(XbtStrategy, {}, 'XBT.LOCAL')
    b.run(strategy_config)
