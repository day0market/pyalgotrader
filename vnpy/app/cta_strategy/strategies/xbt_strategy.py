from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)


class XbtStrategy(CtaTemplate):
    author = " use Python traders "

    fast_window = 10
    slow_window = 20

    fast_ma0 = 0.0
    fast_ma1 = 0.0

    slow_ma0 = 0.0
    slow_ma1 = 0.0

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(XbtStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()
        self._bars_in_pos = 0

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log(" strategy initialization ")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log(" strategy startup ")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log(" stop strategy ")
        self.put_event()

    def on_tick(self, tick: TickData):
        print(f"Tick. Ask: {tick.ask_price_1}. Bid: {tick.bid_price_1}")
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        try:
            prev_high = am.close[-2]
        except IndexError:
            self.put_event()
            return

        if bar.close_price > prev_high and self.pos == 0:
            self.buy(bar.close_price, 1)

        if self.pos != 0:
            self._bars_in_pos += 1
        else:
            self._bars_in_pos = 0

        if self._bars_in_pos == 5:
            self.sell(bar.close_price, 1)

        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
