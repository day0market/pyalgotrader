# Algorithmic Trading
Algorithmic trading can be used to split the list into a small single giant，Can effectively reduce transaction costs，The impact of cost（Iceberg algorithm、Sniper algorithm)；You can also sell high operating within a threshold set(Meshing algorithm、Arbitrage algorithm）。

&nbsp;

## Modules

Algorithmic trading module consists of4Constitute part，As shown below：

- engine：Defined algorithm engine，These include：Engine initialization、Storage/Remove/Loading algorithm configuration、Start algorithm、Stop algorithm、Subscribe Quotes、Hanging withdrawals, etc.。
- template：Template defines the trading algorithm，Specific examples of algorithms，Such as iceberg algorithm，We need to inherit the template。
- algos：Specific examples of trading algorithms。User-based algorithms and templates official is an example algorithm，They can build their own new algorithms。
- ui：based onPyQt5ofGUIGraphics applications。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/algo_trader_document.png)

&nbsp;

## Basic Operations

inVN TraderClick on the menu bar“Features”—>“Algorithmic Trading”It can open the window shown in algorithmic trading module，As shown below。

Algorithmic trading module2Constitute part：
- Escrow，For starting algorithmic trading；
- Data monitoring，For monitoring the implementation of algorithmic trading，And the ability to manually stop the algorithm。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/algo_trader_all_section.png)

&nbsp;

### Escrow

The following algorithm is an example time-weighted average，Detailed below diagram agency transaction options。
- algorithm：Currently offers5Kinds of trading algorithms：Time Weighted Average algorithm、Iceberg algorithm、Sniper algorithm、To delegate、Best price；
- Native code：vt_symbolformat，Such asAAPL.SMART, Subscribe to the formation of prices for algorithmic trading and agency transaction；
- direction：To do more, or short；
- price：Commissioned under the single price；
- Quantity：The total number of delegate，We need to split into small single transaction；
- execution time：The total run time to change the algorithmic trading，In seconds；
- Each round interval：once in a while（second）Commissioned single operation；
- Start algorithm：After setting the algorithms，Algorithms for performing the transaction immediately。

and so，The algorithm performs the following tasks：Time weighted average algorithm，Buy10000shareAAPL（US stocks），Exercise price180Dollars，Execution time600second，Interval6second；That every6Seconds，When buying a price less than or equal180Time，With180The price to buy100shareAAPL，Buy into operation100Secondary。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/trading_section.png)

Trading Configuration can be saved injsonfile，So every time you open algorithmic trading modules do not have to re-enter configuration。Its operations in“Algorithm name”Enter the name of the algorithm settings options，Then click below"Save Settings”Push button。conservedjsonDocumentsC:\Users\Administrator\\.vntraderFolderalgo_trading_setting.jsonin，Figure。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/setting.png)

Commissioned the bottom of the trading interface“Full stop”Button for one-click stop all algorithmic trading execution。

&nbsp;

### Data monitoring

Data monitored by4Constitute a part。

- Active components：Display running algorithmic trading，include：Algorithm name、parameter、status。Rightmost“stop”Button is used to manually stop the execution of algorithms。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/action.png)

&nbsp;

- History delegate assembly：Display algorithm transaction completed，Also included：Algorithm name、parameter、status。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/final.png)

&nbsp;

- Log component：Show splash、stop、Log information related to the completion of the algorithm。After opening algorithmic trading module，Initializes，It will first appear on the log“Algorithmic trading engine start”with“The algorithms loaded successfully”。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/log_section.png)

&nbsp;

- Configuring Components：For loadingalgo_trading_setting.jsonConfiguration information，And displayed in graphical form。
Users can click on“use”Button read configuration information immediately，Commissioned and displayed on the trading interface，Click on“Start algorithm”You can start trading；
Users can also click“Remove”Button to remove the configuration algorithm，Synchronize updates tojsonThe paper。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/setting_section.png)

&nbsp;

## Algorithm example


### Directly commissioned algorithm

Direct issued a new commission（Limit Order、Stop Single、Market Order）

```
    def on_tick(self, tick: TickData):
        """"""
        if not self.vt_orderid:
            if self.direction == Direction.LONG:
                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    self.price,
                    self.volume,
                    self.order_type,
                    self.offset
                )
                
            else:
                self.vt_orderid = self.sell(
                    self.vt_symbol,
                    self.price,
                    self.volume,
                    self.order_type,
                    self.offset
                )
        self.put_variables_event()
```

&nbsp;

### Time Weighted Average algorithm

- The number of commissioned evenly distributed within a certain time zone；
- Pay intervals by hanging the specified price（Or sell orders）。
- Buying case：When buying a price lower than the target price，By placing an order，Takes the minimum value in the remaining number of delegate request amount and dividing the amount of commission。
- Selling situation：When selling a price higher than the target price，By placing an order，Takes the minimum value in the remaining number of delegate request amount and dividing the amount of commission。

```
    def on_timer(self):
        """"""
        self.timer_count += 1
        self.total_count += 1
        self.put_variables_event()

        if self.total_count >= self.time:
            self.write_log("Execution time has ended，Stop algorithm")
            self.stop()
            return

        if self.timer_count < self.interval:
            return
        self.timer_count = 0

        tick = self.get_tick(self.vt_symbol)
        if not tick:
            return

        self.cancel_all()

        left_volume = self.volume - self.traded
        order_volume = min(self.order_volume, left_volume)

        if self.direction == Direction.LONG:
            if tick.ask_price_1 <= self.price:
                self.buy(self.vt_symbol, self.price,
                         order_volume, offset=self.offset)
        else:
            if tick.bid_price_1 >= self.price:
                self.sell(self.vt_symbol, self.price,
                          order_volume, offset=self.offset)
```

&nbsp;

### Iceberg algorithm

- In a pending order price，But only part of hanging，Until all transactions。
- Buying case：Check withdrawals：up to dateTickSell ​​a price lower than the target price，Execute withdrawals；If there is no activity delegates，By placing an order：Commission amount and the remaining amount of commission request amount to hang out in a minimum value。
- Selling situation：Check withdrawals：up to dateTickBuy a price higher than the target price，Execute withdrawals；If there is no activity delegates，By placing an order：Commission amount and the remaining amount of commission request amount to hang out in a minimum value。

```
    def on_timer(self):
        """"""
        self.timer_count += 1

        if self.timer_count < self.interval:
            self.put_variables_event()
            return

        self.timer_count = 0

        contract = self.get_contract(self.vt_symbol)
        if not contract:
            return

        # If order already finished, just send new order
        if not self.vt_orderid:
            order_volume = self.volume - self.traded
            order_volume = min(order_volume, self.display_volume)

            if self.direction == Direction.LONG:
                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )
            else:
                self.vt_orderid = self.sell(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )
        # Otherwise check for cancel
        else:
            if self.direction == Direction.LONG:
                if self.last_tick.ask_price_1 <= self.price:
                    self.cancel_order(self.vt_orderid)
                    self.vt_orderid = ""
                    self.write_log(u"up to dateTickSell ​​a price，Below the purchase order price，Before the commission may be lost，Mandatory withdrawals")
            else:
                if self.last_tick.bid_price_1 >= self.price:
                    self.cancel_order(self.vt_orderid)
                    self.vt_orderid = ""
                    self.write_log(u"up to dateTickBuy a price，Higher than the selling price commission，Before the commission may be lost，Mandatory withdrawals")

        self.put_variables_event()
```

&nbsp;

### Sniper algorithm

- The latest monitoringtickPush the stock market，Immediately found a good price deal offer。
- Buying case：up to dateTickWhen selling a price lower than the target price，By placing an order，Takes the minimum value with a number of commission in the amount of sales commission amount remaining。
- Selling situation：up to dateTickWhen buying a price higher than the target price，By placing an order，Takes the minimum value in the number of delegation request amount to a remaining amount of the buy。

```
    def on_tick(self, tick: TickData):
        """"""
        if self.vt_orderid:
            self.cancel_all()
            return

        if self.direction == Direction.LONG:
            if tick.ask_price_1 <= self.price:
                order_volume = self.volume - self.traded
                order_volume = min(order_volume, tick.ask_volume_1)

                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )
        else:
            if tick.bid_price_1 >= self.price:
                order_volume = self.volume - self.traded
                order_volume = min(order_volume, tick.bid_volume_1)

                self.vt_orderid = self.sell(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )

        self.put_variables_event()
```

&nbsp;

### Conditions commissioned algorithm

- The latest monitoringtickPush the stock market，Quotes found immediately offer breakthrough deal。
- Buying case：TickWhen the latest price is higher than the target price，By placing an order，Commissioned price target price plus the super price。
- Selling situation：TickWhen the new price is lower than the target price，By placing an order，Commissioned price target price minus the super price。

```
    def on_tick(self, tick: TickData):
        """"""
        if self.vt_orderid:
            return

        if self.direction == Direction.LONG:
            if tick.last_price >= self.stop_price:
                price = self.stop_price + self.price_add

                if tick.limit_up:
                    price = min(price, tick.limit_up)

                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    price,
                    self.volume,
                    offset=self.offset
                )
                self.write_log(f"Stop order has been triggered，Code：{self.vt_symbol}，direction：{self.direction}, price：{self.stop_price}，Quantity：{self.volume}，Kaiping：{self.offset}")                   

        else:
            if tick.last_price <= self.stop_price:
                price = self.stop_price - self.price_add
                
                if tick.limit_down:
                    price = max(price, tick.limit_down)

                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    price,
                    self.volume,
                    offset=self.offset
                )
                self.write_log(f"Stop order has been triggered，Code：{self.vt_symbol}，direction：{self.direction}, price：{self.stop_price}，Quantity：{self.volume}，Kaiping：{self.offset}") 

        self.put_variables_event()
```

&nbsp;

### Best price algorithm

- The latest monitoringtickPush the stock market，Immediately found a good price deal offer。
- Buying case：Check withdrawals：up to dateTickWhen buying a price is not equal to the target price，Execute withdrawals；If there is no activity delegates，By placing an order：Commissioned for the latest priceTickBuy a price，Commission amount remaining number of delegate。
- Selling situation：Check withdrawals：up to dateTickWhen buying a price is not equal to the target price，Execute withdrawals；If there is no activity delegates，By placing an order：Commissioned for the latest priceTickSell ​​a price，Commission amount remaining number of delegate。

```
    def on_tick(self, tick: TickData):
        """"""
        self.last_tick = tick

        if self.direction == Direction.LONG:
            if not self.vt_orderid:
                self.buy_best_limit()
            elif self.order_price != self.last_tick.bid_price_1:
                self.cancel_all()
        else:
            if not self.vt_orderid:
                self.sell_best_limit()
            elif self.order_price != self.last_tick.ask_price_1:
                self.cancel_all()

        self.put_variables_event()

    def buy_best_limit(self):
        """"""
        order_volume = self.volume - self.traded
        self.order_price = self.last_tick.bid_price_1
        self.vt_orderid = self.buy(
            self.vt_symbol,
            self.order_price,
            order_volume,
            offset=self.offset
        )        

    def sell_best_limit(self):
        """"""
        order_volume = self.volume - self.traded
        self.order_price = self.last_tick.ask_price_1
        self.vt_orderid = self.sell(
            self.vt_symbol,
            self.order_price,
            order_volume,
            offset=self.offset
        ) 
```

&nbsp;

### Meshing algorithm

- Periodically check the commission case，If a delegate to empty。
- Stepping based on price set by the user（That grid）Calculating a target distance，Target distance=（target price- Current price）/Stepping price，Therefore, the current price is below the target price，Target distance is positive，Direction to buy；The current price is higher than the target price，Target distance is negative，Direction to sell。（Buy low sell high concept）
- Calculating a target position，Target positions= Obtaining a desired distance after the whole * The number of commissioned stepping。Note Sell seller is rounding a manner different from：To buy rounded down directionmath.floor()，As the target distance1.6，take1；To round up direction sell，As the target distance-1.6，take-1。
- Calculate specific delegate positions：If the goal of buying positions greater than the current position，Perform operations to buy；If the target sell positions below the current position，Sell ​​operations to perform。
- In order to be able to quickly deal，Buying case is based onask priceCompute，Sell ​​is based on the casebid priceCompute。


```
    def on_timer(self):
        """"""
        if not self.last_tick:
            return

        self.timer_count += 1
        if self.timer_count < self.interval:
            self.put_variables_event()
            return        
        self.timer_count = 0
        
        if self.vt_orderid:
            self.cancel_all()        

        # Calculate target volume to buy
        target_buy_distance = (self.price - self.last_tick.ask_price_1) / self.step_price
        target_buy_position = math.floor(target_buy_distance) * self.step_volume
        target_buy_volume = target_buy_position - self.last_pos

        # Buy when price dropping
        if target_buy_volume > 0:
            self.vt_orderid = self.buy(
                self.vt_symbol,
                self.last_tick.ask_price_1,
                min(target_buy_volume, self.last_tick.ask_volume_1)
            )
        
        # Calculate target volume to sell
        target_sell_distance = (self.price - self.last_tick.bid_price_1) / self.step_price
        target_sell_position = math.ceil(target_sell_distance) * self.step_volume
        target_sell_volume = self.last_pos - target_sell_position

        # Sell when price rising
        if target_sell_volume > 0:
            self.vt_orderid = self.sell(
                self.vt_symbol,
                self.last_tick.bid_price_1,
                min(target_sell_volume, self.last_tick.bid_volume_1)
            )
```

&nbsp;

### Arbitrage algorithm

- Periodically check the commission case，If a delegate to empty；If the initiative also holds the leg net position，By passive leg transaction to hedge。
- Computing spreadsspread_bid_price with spread_ask_price, And a corresponding number of commission
- Selling situation：Initiative leg relatively passive leg up，Its spreadspread_bid_pricemore than thespread_upTime，Trigger a buy signal
- Buying case：Initiative leg relatively passive leg down，Its spreadspread_ask_priceLess than - spread_down(spread_downThe default setting is a positive number)Time，Trigger a sell signal
- Join the largest positions in the trading signals to determine restrictions，Its role is to avoid excessive positions or lead to a margin call directly Exchange punitive strong level；And with the continued volatility spreads，Initiative leg positions from0 -> 10 -> 0 -> -10 -> 0,Enabling open profit taking。


```
    def on_timer(self):
        """"""
        self.timer_count += 1
        if self.timer_count < self.interval:
            self.put_variables_event()
            return
        self.timer_count = 0

        if self.active_vt_orderid or self.passive_vt_orderid:
            self.cancel_all()
            return
        
        if self.net_pos:
            self.hedge()
            return
      
        active_tick = self.get_tick(self.active_vt_symbol)
        passive_tick = self.get_tick(self.passive_vt_symbol)
        if not active_tick or not passive_tick:
            return

        # Calculate spread
        spread_bid_price = active_tick.bid_price_1 - passive_tick.ask_price_1
        spread_ask_price = active_tick.ask_price_1 - passive_tick.bid_price_1

        spread_bid_volume = min(active_tick.bid_volume_1, passive_tick.ask_volume_1)
        spread_ask_volume = min(active_tick.ask_volume_1, passive_tick.bid_volume_1)

        # Sell condition      
        if spread_bid_price > self.spread_up:
            if self.acum_pos <= -self.max_pos:
                return
            else:
                self.active_vt_orderid = self.sell(
                    self.active_vt_symbol,
                    active_tick.bid_price_1,
                    spread_bid_volume               
                )

        # Buy condition
        elif spread_ask_price < -self.spread_down:
            if self.acum_pos >= self.max_pos:
                return
            else:
                self.active_vt_orderid = self.buy(
                    self.active_vt_symbol,
                    active_tick.ask_price_1,
                    spread_ask_volume
                )
        self.put_variables_event()
    
    def hedge(self):
        """"""
        tick = self.get_tick(self.passive_vt_symbol)
        volume = abs(self.net_pos)

        if self.net_pos > 0:
            self.passive_vt_orderid = self.sell(
                self.passive_vt_symbol,
                tick.bid_price_5,
                volume
            )
        elif self.net_pos < 0:
            self.passive_vt_orderid = self.buy(
                self.passive_vt_symbol,
                tick.ask_price_5,
                volume
            )

    def on_trade(self, trade: TradeData):
        """"""
        # Update net position volume
        if trade.direction == Direction.LONG:
            self.net_pos += trade.volume
        else:
            self.net_pos -= trade.volume

        # Update active symbol position           
        if trade.vt_symbol == self.active_vt_symbol:
            if trade.direction == Direction.LONG:
                self.acum_pos += trade.volume
            else:
                self.acum_pos -= trade.volume

        # Hedge if active symbol traded     
        if trade.vt_symbol == self.active_vt_symbol:
            self.hedge()
        
        self.put_variables_event()

```