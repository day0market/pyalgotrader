#  algorithmic trading 
 algorithmic trading can be used to split the list into a small single giant ， can effectively reduce transaction costs ， the impact of cost （ iceberg algorithm ,  sniper algorithm )； you can also sell high operating within a threshold set ( meshing algorithm ,  arbitrage algorithm ）. 

&nbsp;

##  modules 

 algorithmic trading module consists of 4 constitute part ， as shown below ：

- engine： defined algorithm engine ， these include ： engine initialization ,  storage / remove / loading algorithm configuration ,  start algorithm ,  stop algorithm ,  subscribe quotes ,  hanging withdrawals, etc. . 
- template： template defines the trading algorithm ， specific examples of algorithms ， such as iceberg algorithm ， we need to inherit the template . 
- algos： specific examples of trading algorithms .  user-based algorithms and templates official is an example algorithm ， they can build their own new algorithms . 
- ui： based on PyQt5 of GUI graphics applications . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/algo_trader_document.png)

&nbsp;

##  basic operations 

 in VN Trader click on the menu bar “ features ”—>“ algorithmic trading ” it can open the window shown in algorithmic trading module ， as shown below . 

 algorithmic trading module 2 constitute part ：
-  escrow ， for starting algorithmic trading ；
-  data monitoring ， for monitoring the implementation of algorithmic trading ， and the ability to manually stop the algorithm . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/algo_trader_all_section.png)

&nbsp;

###  escrow 

 the following algorithm is an example time-weighted average ， detailed below diagram agency transaction options . 
-  algorithm ： currently offers 5 kinds of trading algorithms ： time weighted average algorithm ,  iceberg algorithm ,  sniper algorithm ,  to delegate ,  best price ；
-  native code ：vt_symbol format ， such as AAPL.SMART,  subscribe to the formation of prices for algorithmic trading and agency transaction ；
-  direction ： to do more, or short ；
-  price ： commissioned under the single price ；
-  quantity ： the total number of delegate ， we need to split into small single transaction ；
-  execution time ： the total run time to change the algorithmic trading ， in seconds ；
-  each round interval ： once in a while （ second ） commissioned single operation ；
-  start algorithm ： after setting the algorithms ， algorithms for performing the transaction immediately . 

 and so ， the algorithm performs the following tasks ： time weighted average algorithm ， buy 10000 share AAPL（ us stocks ）， exercise price 180 dollars ， execution time 600 second ， interval 6 second ； that every 6 seconds ， when buying a price less than or equal 180 time ， with 180 the price to buy 100 share AAPL， buy into operation 100 secondary . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/trading_section.png)

 trading configuration can be saved in json file ， so every time you open algorithmic trading modules do not have to re-enter configuration .  its operations in “ algorithm name ” enter the name of the algorithm settings options ， then click below " save settings ” push button .  conserved json documents C:\Users\Administrator\\.vntrader folder algo_trading_setting.json in ， figure . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/setting.png)

 commissioned the bottom of the trading interface “ full stop ” button for one-click stop all algorithmic trading execution . 

&nbsp;

###  data monitoring 

 data monitored by 4 constitute a part . 

-  active components ： display running algorithmic trading ， include ： algorithm name ,  parameter ,  status .  rightmost “ stop ” button is used to manually stop the execution of algorithms . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/action.png)

&nbsp;

-  history delegate assembly ： display algorithm transaction completed ， also included ： algorithm name ,  parameter ,  status . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/final.png)

&nbsp;

-  log component ： show splash ,  stop ,  log information related to the completion of the algorithm .  after opening algorithmic trading module ， initializes ， it will first appear on the log “ algorithmic trading engine start ” with “ the algorithms loaded successfully ”. 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/log_section.png)

&nbsp;

-  configuring components ： for loading algo_trading_setting.json configuration information ， and displayed in graphical form . 
 users can click on “ use ” button read configuration information immediately ， commissioned and displayed on the trading interface ， click on “ start algorithm ” you can start trading ；
 users can also click “ remove ” button to remove the configuration algorithm ， synchronize updates to json the paper . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/setting_section.png)

&nbsp;

##  algorithm example 


###  directly commissioned algorithm 

 direct issued a new commission （ limit order ,  stop single ,  market order ）

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

###  time weighted average algorithm 

-  the number of commissioned evenly distributed within a certain time zone ；
-  pay intervals by hanging the specified price （ or sell orders ）. 
-  buying case ： when buying a price lower than the target price ， by placing an order ， takes the minimum value in the remaining number of delegate request amount and dividing the amount of commission . 
-  selling situation ： when selling a price higher than the target price ， by placing an order ， takes the minimum value in the remaining number of delegate request amount and dividing the amount of commission . 

```
    def on_timer(self):
        """"""
        self.timer_count += 1
        self.total_count += 1
        self.put_variables_event()

        if self.total_count >= self.time:
            self.write_log(" execution time has ended ， stop algorithm ")
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

###  iceberg algorithm 

-  in a pending order price ， but only part of hanging ， until all transactions . 
-  buying case ： check withdrawals ： up to date Tick sell ​​a price lower than the target price ， execute withdrawals ； if there is no activity delegates ， by placing an order ： commission amount and the remaining amount of commission request amount to hang out in a minimum value . 
-  selling situation ： check withdrawals ： up to date Tick buy a price higher than the target price ， execute withdrawals ； if there is no activity delegates ， by placing an order ： commission amount and the remaining amount of commission request amount to hang out in a minimum value . 

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
                    self.write_log(u" up to date Tick sell ​​a price ， below the purchase order price ， before the commission may be lost ， mandatory withdrawals ")
            else:
                if self.last_tick.bid_price_1 >= self.price:
                    self.cancel_order(self.vt_orderid)
                    self.vt_orderid = ""
                    self.write_log(u" up to date Tick buy a price ， higher than the selling price commission ， before the commission may be lost ， mandatory withdrawals ")

        self.put_variables_event()
```

&nbsp;

###  sniper algorithm 

-  the latest monitoring tick push the stock market ， immediately found a good price deal offer . 
-  buying case ： up to date Tick when selling a price lower than the target price ， by placing an order ， takes the minimum value with a number of commission in the amount of sales commission amount remaining . 
-  selling situation ： up to date Tick when buying a price higher than the target price ， by placing an order ， takes the minimum value in the number of delegation request amount to a remaining amount of the buy . 

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

###  conditions commissioned algorithm 

-  the latest monitoring tick push the stock market ， quotes found immediately offer breakthrough deal . 
-  buying case ：Tick when the latest price is higher than the target price ， by placing an order ， commissioned price target price plus the super price . 
-  selling situation ：Tick when the new price is lower than the target price ， by placing an order ， commissioned price target price minus the super price . 

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
                self.write_log(f" stop order has been triggered ， code ：{self.vt_symbol}， direction ：{self.direction},  price ：{self.stop_price}， quantity ：{self.volume}， kaiping ：{self.offset}")                   

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
                self.write_log(f" stop order has been triggered ， code ：{self.vt_symbol}， direction ：{self.direction},  price ：{self.stop_price}， quantity ：{self.volume}， kaiping ：{self.offset}") 

        self.put_variables_event()
```

&nbsp;

###  best price algorithm 

-  the latest monitoring tick push the stock market ， immediately found a good price deal offer . 
-  buying case ： check withdrawals ： up to date Tick when buying a price is not equal to the target price ， execute withdrawals ； if there is no activity delegates ， by placing an order ： commissioned for the latest price Tick buy a price ， commission amount remaining number of delegate . 
-  selling situation ： check withdrawals ： up to date Tick when buying a price is not equal to the target price ， execute withdrawals ； if there is no activity delegates ， by placing an order ： commissioned for the latest price Tick sell ​​a price ， commission amount remaining number of delegate . 

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

###  meshing algorithm 

-  periodically check the commission case ， if a delegate to empty . 
-  stepping based on price set by the user （ that grid ） calculating a target distance ， target distance =（ target price -  current price ）/ stepping price ， therefore, the current price is below the target price ， target distance is positive ， direction to buy ； the current price is higher than the target price ， target distance is negative ， direction to sell . （ buy low sell high concept ）
-  calculating a target position ， target positions =  obtaining a desired distance after the whole  *  the number of commissioned stepping .  note sell seller is rounding a manner different from ： to buy rounded down direction math.floor()， as the target distance 1.6， take 1； to round up direction sell ， as the target distance -1.6， take -1. 
-  calculate specific delegate positions ： if the goal of buying positions greater than the current position ， perform operations to buy ； if the target sell positions below the current position ， sell ​​operations to perform . 
-  in order to be able to quickly deal ， buying case is based on ask price compute ， sell ​​is based on the case bid price compute . 


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

###  arbitrage algorithm 

-  periodically check the commission case ， if a delegate to empty ； if the initiative also holds the leg net position ， by passive leg transaction to hedge . 
-  computing spreads spread_bid_price  with  spread_ask_price,  and a corresponding number of commission 
-  selling situation ： initiative leg relatively passive leg up ， its spread spread_bid_price more than the spread_up time ， trigger a buy signal 
-  buying case ： initiative leg relatively passive leg down ， its spread spread_ask_price less than  - spread_down(spread_down the default setting is a positive number ) time ， trigger a sell signal 
-  join the largest positions in the trading signals to determine restrictions ， its role is to avoid excessive positions or lead to a margin call directly exchange punitive strong level ； and with the continued volatility spreads ， initiative leg positions from 0 -> 10 -> 0 -> -10 -> 0, enabling open profit taking . 


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