from vnpy.trader.constant import Direction
from vnpy.trader.object import TradeData, OrderData
from vnpy.trader.engine import BaseEngine

from vnpy.app.algo_trading import AlgoTemplate


class ArbitrageAlgo(AlgoTemplate):
    """"""

    display_name = "Arbitrage  arbitrage "

    default_setting = {
        "active_vt_symbol": "",
        "passive_vt_symbol": "",
        "spread_up": 0.0,
        "spread_down": 0.0,
        "max_pos": 0,
        "interval": 0,
    }

    variables = [
        "timer_count",
        "active_vt_orderid",
        "passive_vt_orderid",
        "active_pos",
        "passive_pos"
    ]

    def __init__(
        self,
        algo_engine: BaseEngine,
        algo_name: str,
        setting: dict
    ):
        """"""
        super().__init__(algo_engine, algo_name, setting)

        # Parameters
        self.active_vt_symbol = setting["active_vt_symbol"]
        self.passive_vt_symbol = setting["passive_vt_symbol"]
        self.spread_up = setting["spread_up"]
        self.spread_down = setting["spread_down"]
        self.max_pos = setting["max_pos"]
        self.interval = setting["interval"]

        # Variables
        self.active_vt_orderid = ""
        self.passive_vt_orderid = ""
        self.active_pos = 0
        self.passive_pos = 0
        self.timer_count = 0

        self.subscribe(self.active_vt_symbol)
        self.subscribe(self.passive_vt_symbol)

        self.put_parameters_event()
        self.put_variables_event()

    def on_stop(self):
        """"""
        self.write_log(" stop algorithm ")

    def on_order(self, order: OrderData):
        """"""
        if order.vt_symbol == self.active_vt_symbol:
            if not order.is_active():
                self.active_vt_orderid = ""
        elif order.vt_symbol == self.passive_vt_symbol:
            if not order.is_active():
                self.passive_vt_orderid = ""
        self.put_variables_event()

    def on_trade(self, trade: TradeData):
        """"""
        # Update pos
        if trade.direction == Direction.LONG:
            if trade.vt_symbol == self.active_vt_symbol:
                self.active_pos += trade.volume
            else:
                self.passive_pos += trade.volume
        else:
            if trade.vt_symbol == self.active_vt_symbol:
                self.active_pos -= trade.volume
            else:
                self.passive_pos -= trade.volume

        # Hedge if active symbol traded
        if trade.vt_symbol == self.active_vt_symbol:
            self.write_log(" actively traded in return receive leg ， hedge execution ")
            self.hedge()

        self.put_variables_event()

    def on_timer(self):
        """"""
        # Run algo by fixed interval
        self.timer_count += 1
        if self.timer_count < self.interval:
            self.put_variables_event()
            return
        self.timer_count = 0

        # Cancel all active orders before moving on
        if self.active_vt_orderid or self.passive_vt_orderid:
            self.write_log(" there are not traded commissioned ， execute withdrawals ")
            self.cancel_all()
            return

        # Make sure that active leg is fully hedged by passive leg
        if (self.active_pos + self.passive_pos) != 0:
            self.write_log(" inconsistent number of active and passive leg leg ， hedge execution ")
            self.hedge()
            return

        # Make sure that tick data of both leg are available
        active_tick = self.get_tick(self.active_vt_symbol)
        passive_tick = self.get_tick(self.passive_vt_symbol)
        if not active_tick or not passive_tick:
            self.write_log(" get a leg bar arbitrage market failure ， unable to trade ")
            return

        # Calculate spread
        spread_bid_price = active_tick.bid_price_1 - passive_tick.ask_price_1
        spread_ask_price = active_tick.ask_price_1 - passive_tick.bid_price_1

        spread_bid_volume = min(active_tick.bid_volume_1,
                                passive_tick.ask_volume_1)
        spread_ask_volume = min(active_tick.ask_volume_1,
                                passive_tick.bid_volume_1)

        msg = f" spread handicap ， buy ：{spread_bid_price} ({spread_bid_volume})， sell ：{spread_ask_price} ({spread_ask_volume})"
        self.write_log(msg)

        # Sell condition
        if spread_bid_price > self.spread_up:
            self.write_log(" arbitrage spreads over the upper limit ， meet short condition ")

            if self.active_pos > -self.max_pos:
                self.write_log(" the current position is less than the maximum position limits ， sell ​​operations to perform ")

                volume = min(spread_bid_volume,
                             self.active_pos + self.max_pos)

                self.active_vt_orderid = self.sell(
                    self.active_vt_symbol,
                    active_tick.bid_price_1,
                    volume
                )

        # Buy condition
        elif spread_ask_price < -self.spread_down:
            self.write_log(" arbitrage spreads over limit ， do more conditions are met ")

            if self.active_pos < self.max_pos:
                self.write_log(" the current position is less than the maximum position limits ， perform operations to buy ")

                volume = min(spread_ask_volume,
                             self.max_pos - self.active_pos)

                self.active_vt_orderid = self.buy(
                    self.active_vt_symbol,
                    active_tick.ask_price_1,
                    volume
                )

        # Update GUI
        self.put_variables_event()

    def hedge(self):
        """"""
        tick = self.get_tick(self.passive_vt_symbol)
        volume = -self.active_pos - self.passive_pos

        if volume > 0:
            self.passive_vt_orderid = self.buy(
                self.passive_vt_symbol,
                tick.ask_price_1,
                volume
            )
        elif volume < 0:
            self.passive_vt_orderid = self.sell(
                self.passive_vt_symbol,
                tick.bid_price_1,
                abs(volume)
            )
