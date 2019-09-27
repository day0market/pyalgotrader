# CTA policy module 


##  modules 

CTA mainly by the policy module 7 constitute part ， as shown below ：

- base： defined CTA module used in some of the basic settings ， such as engine type （ backtesting / firm ）,  back to the measurement mode （K line /Tick）,  local single stop and a stop order status definitions （ waiting / revoked / triggered ）. 
  
- template： defined CTA policy template （ it includes signal generation and delegate management ）, CTA signal （ it is only responsible for signal generation ）,  target position algorithm （ only responsible for delegated administration ， it applies to split the giant commission ， reduce the cost impact ）. 
- strategies:  the official provided cta policy example ， it contains double the average from the most basic strategy ， to channel breakout type of strategy bollinger bands ， the strategy across time periods ， then the signal generation and delegated administration open to independent multi-signal strategy . ( user-defined strategy can be placed strategies folder run )
- backesting： it includes backtesting engine and parameter optimization .  backtesting engine which defines the data load ,  commissioned matching mechanism ,  calculation and statistical indicators related to profitability ,  results plotting other functions . 
- converter： it defines this level for the period of the species / flat commission mode conversion module yesterday ； for users of other species can also optional parameters lock lock mode switch to . 
- engine： defined CTA strategy firm engine ， these include ：RQData the client initialization and loading data ,  strategies and start initialization ,  push Tick subscribe to the policy market ,  hanging cancellation operation ,  strategies such as stop and remove . 
- ui： based on PyQt5 of GUI graphics applications . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_strategy/seix_elementos.png "enter image title here")

&nbsp;

##  loading 

 in the real dish ，RQData initialized strategy through real-time load data .  the main function in CTA firm engine engine.py in the realization . 
 here are the specific process ：
-  in the menu bar click “ configuration ”， enter the global configuration page input RQData account password ； or direct configuration json file ， that is under the user's directory .vntrader folders found vt_setting.json， figure . 
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_strategy/RQData_setting.png "enter image title here")

-  initialization RQData client ： from vt_setting.json read RQData account ,  password to rq_client.init() function initializes 

```
    def init_rqdata(self):
        """
        Init RQData client.
        """
        username = SETTINGS["rqdata.username"]
        password = SETTINGS["rqdata.password"]
        if not username or not password:
            return

        import rqdatac
        
        self.rq_client = rqdatac
        self.rq_client.init(username, password,
                            ('rqdatad-pro.ricequant.com', 16011))
```


- RQData loading data firm ： entry vt_symbol rear ， first in line will be converted to RQData formats rq_symbol， by get_price() download data function ， and inserted into the database . 
  
```
    def query_bar_from_rq(
        self, vt_symbol: str, interval: Interval, start: datetime, end: datetime
    ):
        """
        Query bar data from RQData.
        """
        symbol, exchange_str = vt_symbol.split(".")
        rq_symbol = to_rq_symbol(vt_symbol)
        if rq_symbol not in self.rq_symbols:
            return None
        
        end += timedelta(1)     # For querying night trading period data

        df = self.rq_client.get_price(
            rq_symbol,
            frequency=interval.value,
            fields=["open", "high", "low", "close", "volume"],
            start_date=start,
            end_date=end
        )

        data = []
        for ix, row in df.iterrows():
            bar = BarData(
                symbol=symbol,
                exchange=Exchange(exchange_str),
                interval=interval,
                datetime=row.name.to_pydatetime(),
                open_price=row["open"],
                high_price=row["high"],
                low_price=row["low"],
                close_price=row["close"],
                volume=row["volume"],
                gateway_name="RQ"
            )
            data.append(bar)
```

&nbsp;

##  strategy development 
CTA policy templates provide a complete signal generation and delegate management functions ， users can develop their own strategies based on the template .  the new strategy can be placed in the user runs the file （ recommend ）， as in c:\users\administrator.vntrader create a directory strategies folder ； it can be placed in the root directory vnpy\app\cta_strategy\strategies folder . 
 note ： policy file is named underline mode ， such as boll_channel_strategy.py； the policy class name is used in camel ， such as BollChannelStrategy. 

 by the following BollChannelStrategy policy example ， concrete steps to demonstrate the development strategy ：

###  parameter settings 

 define policy parameters and policy variables initialized .  policy parameters for the class policy of public property ， users can call or change policy parameters by creating a new instance . 

 as for rb1905 variety ， users can create based on BollChannelStrategy examples of strategies ， such as RB_BollChannelStrategy，boll_window it can be made 18 change 30. 

 examples of ways to create strategies to effectively implement a strategy to run a number of varieties ， policy parameters and which can be adjusted by the features of species . 
```
    boll_window = 18
    boll_dev = 3.4
    cci_window = 10
    atr_window = 30
    sl_multiplier = 5.2
    fixed_size = 1

    boll_up = 0
    boll_down = 0
    cci_value = 0
    atr_value = 0

    intra_trade_high = 0
    intra_trade_low = 0
    long_stop = 0
    short_stop = 0
```

###  initialization class 
 initialization points 3 step ：
-  by super( ) the methods are inherited CTA policy template ， in __init__( ) incoming function CTA engine ,  policy name , vt_symbol,  parameter settings . 
-  transfer K line generation module : by the time slices Tick data synthesis 1 minute K line data ， then a larger time period data ， such as 15 minute K line . 
-  transfer K line time sequence manager module ： based on K line data ， such as 1 minute , 15 minute ， to form the corresponding technical specifications . 
  
```
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(BollChannelStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )

        self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am = ArrayManager()
```

###  initialization policy ,  start up ,  stop 
 by “CTA tactics ” button component-related functions to achieve . 

 note ： function load_bar(10)， on behalf of the policy needs to load initialization 10 trading historical data .  the historical data can be Tick data ， can also be K line data .  in the initialization time strategy ， will call K calculating line time sequence manager and cache related calculation index ， but the transaction does not trigger . 

```
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
        self.write_log(" policy startup ")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log(" stop strategy ")
```
### Tick data return 
 subscribe to a variety of tactics contract market ， exchange will push Tick the data on policy . 

 due to BollChannelStrategy is based on 15 minute K generating a signal line transactions ， it is received Tick after data ， need to use K line generation module inside update_tick function ， by a method of time-slicing ， polymerized into 1 minute K line data ， and push on_bar function . 

```
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)
```

### K line data return 

 receive push over 1 minute K after the data line ， by K line generation module inside update_bar function ， the method of minutes to slice ， synthesis 15 minute K line data ， and push on_15min_bar function . 
```
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)
```

### 15 minute K line data return 

 be responsible for CTA generating a signal ， by 3 parts ：
-  clear unsold commissioned ： in order to prevent under the list before a 15 minutes no deal ， but next 15 minutes may have adjusted the price ， then apply cancel_all() unsold method previously withdrawn all at once commissioned ， this is to ensure that the current strategy 15 the entire state of minutes and only began to be clear . 
-  transfer K line time sequence manager module ： based on the latest 15 minute K calculating respective line data calculation index ， the vertical rail bollinger band channel , CCI index , ATR index 
-  signal calculation ： and by determining the binding positions CCI index ,  bollinger band channel , ATR indicators point to hang out in the channel breakout single delegate stop （buy/sell)， at the same time set the departure point (short/cover). 

 note ：CTA strategy with specific low and high winning percentage than the profit and loss ： in the case of difficult to improve the odds of ， research strategies to enhance profit and loss ratio in favor of increased profitability strategy . 

```
    def on_15min_bar(self, bar: BarData):
        """"""
        self.cancel_all()

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.boll_up, self.boll_down = am.boll(self.boll_window, self.boll_dev)
        self.cci_value = am.cci(self.cci_window)
        self.atr_value = am.atr(self.atr_window)

        if self.pos == 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = bar.low_price

            if self.cci_value > 0:
                self.buy(self.boll_up, self.fixed_size, True)
            elif self.cci_value < 0:
                self.short(self.boll_down, self.fixed_size, True)

        elif self.pos > 0:
            self.intra_trade_high = max(self.intra_trade_high, bar.high_price)
            self.intra_trade_low = bar.low_price

            self.long_stop = self.intra_trade_high - self.atr_value * self.sl_multiplier
            self.sell(self.long_stop, abs(self.pos), True)

        elif self.pos < 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = min(self.intra_trade_low, bar.low_price)

            self.short_stop = self.intra_trade_low + self.atr_value * self.sl_multiplier
            self.cover(self.short_stop, abs(self.pos), True)

        self.put_event()
```

###  return commission ,  return on turnover ,  one-stop return 

 in the policy can be directly pass， the specific application logic to back-test / firm responsible for engine . 
```
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
```




&nbsp;

##  research measured back 
backtesting.py it defines the backtesting engine ， the following describes the functions related functions ， backtesting engine and application examples ：

###  loading strategy 

 the CTA policy logic ， the corresponding contract variety ， and parameter settings （ can be modified outside the policy file ） loaded into the back-tested engine . 
```
    def add_strategy(self, strategy_class: type, setting: dict):
        """"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self, strategy_class.__name__, self.vt_symbol, setting
        )
```
&nbsp;

###  loading historical data 

 responsible for loading historical data corresponding to species ， roughly has 4 steps ：
-  the different data types ， divided K wire mode and Tick mode ；
-  by select().where() method ， conditionally select data from the database ， which includes screening criteria ：vt_symbol,   backtesting start date ,  backtesting end date , K line cycle （K offline mode ）；
- order_by(DbBarData.datetime) it represents the data to be loaded chronologically ；
-  loading data is carried out in an iterative manner ， the final data is stored self.history_data. 

```
    def load_data(self):
        """"""
        self.output(" begins loading historical data ")

        if self.mode == BacktestingMode.BAR:
            s = (
                DbBarData.select()
                .where(
                    (DbBarData.vt_symbol == self.vt_symbol) 
                    & (DbBarData.interval == self.interval) 
                    & (DbBarData.datetime >= self.start) 
                    & (DbBarData.datetime <= self.end)
                )
                .order_by(DbBarData.datetime)
            )
            self.history_data = [db_bar.to_bar() for db_bar in s]
        else:
            s = (
                DbTickData.select()
                .where(
                    (DbTickData.vt_symbol == self.vt_symbol) 
                    & (DbTickData.datetime >= self.start) 
                    & (DbTickData.datetime <= self.end)
                )
                .order_by(DbTickData.datetime)
            )
            self.history_data = [db_tick.to_tick() for db_tick in s]

        self.output(f" historical data loaded ， the amount of data ：{len(self.history_data)}")
```
&nbsp;

###  brokered transactions 

 loading CTA after strategies and relevant historical data ， strategy related indicators will be calculated according to the latest data .  if they meet the conditions will generate trading signals ， issued a specific commission （buy/sell/short/cover）， and the next one K line auction . 

 depending on the type of delegate ， backtesting engine provides 2 brokered transactions kinds of mechanisms to try to imitate the real trade links ：

-  limit orders brokered transactions ：（ direction, for example to buy ） first determine whether the transaction occurred ， standard price for the transaction commission >=  under a K the lowest line ； then determine the transaction price ， price and the transaction price was commissioned at a K minimum line opening price . 

-  stop single brokered transactions ：（ direction, for example to buy ） first determine whether the transaction occurred ， standard price for the transaction commission <=  under a K the highest price line ； then determine the transaction price ， price and the transaction price was commissioned at a K maximum line opening price . 

&nbsp;

 the following shows the engine limit orders brokered transactions process ：
-  brokered transactions will determine the price ；
-  all limit order limit order traversal dictionary ， push commissioned into the transaction queue status is not updated ；
-  analyzing transaction status ， if there is turnover ， push transaction data and commission data ；
-  delete turnover limit orders from the dictionary . 

```
    def cross_limit_order(self):
        """
        Cross limit order with last bar/tick data.
        """
        if self.mode == BacktestingMode.BAR:
            long_cross_price = self.bar.low_price
            short_cross_price = self.bar.high_price
            long_best_price = self.bar.open_price
            short_best_price = self.bar.open_price
        else:
            long_cross_price = self.tick.ask_price_1
            short_cross_price = self.tick.bid_price_1
            long_best_price = long_cross_price
            short_best_price = short_cross_price

        for order in list(self.active_limit_orders.values()):
            # Push order update with status "not traded" (pending)
            if order.status == Status.SUBMITTING:
                order.status = Status.NOTTRADED
                self.strategy.on_order(order)

            # Check whether limit orders can be filled.
            long_cross = (
                order.direction == Direction.LONG 
                and order.price >= long_cross_price 
                and long_cross_price > 0
            )

            short_cross = (
                order.direction == Direction.SHORT 
                and order.price <= short_cross_price 
                and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            # Push order udpate with status "all traded" (filled).
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.on_order(order)

            self.active_limit_orders.pop(order.vt_orderid)

            # Push trade update
            self.trade_count += 1

            if long_cross:
                trade_price = min(order.price, long_best_price)
                pos_change = order.volume
            else:
                trade_price = max(order.price, short_best_price)
                pos_change = -order.volume

            trade = TradeData(
                symbol=order.symbol,
                exchange=order.exchange,
                orderid=order.orderid,
                tradeid=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                time=self.datetime.strftime("%H:%M:%S"),
                gateway_name=self.gateway_name,
            )
            trade.datetime = self.datetime

            self.strategy.pos += pos_change
            self.strategy.on_trade(trade)

            self.trades[trade.vt_tradeid] = trade
```

&nbsp;

###  profit and loss calculation method 

 based on the closing price ,  day positions ,  contract size ,  slippage ,  calculate the total commission rate gains and losses and net gains and losses ， and the calculation result DataFrame output format ， complete statistics based on mark-to-market gains and losses . 

 the following shows the calculation of profit and loss 

-  floating profit and loss  =  positions  \*（ closing price  -  yesterday's closing price ）\*   contract size 
-  the actual profit and loss  =  the amount of change positions   \* （ at that time the closing price  -  open price ）\*  contract size 
-  total profit and loss  =  floating profit and loss  +  the actual profit and loss 
-  net profit and loss  =  total profit and loss  -  total fee  -  the total slippage 

```
    def calculate_pnl(
        self,
        pre_close: float,
        start_pos: float,
        size: int,
        rate: float,
        slippage: float,
    ):
        """"""
        self.pre_close = pre_close

        # Holding pnl is the pnl from holding position at day start
        self.start_pos = start_pos
        self.end_pos = start_pos
        self.holding_pnl = self.start_pos * \
            (self.close_price - self.pre_close) * size

        # Trading pnl is the pnl from new trade during the day
        self.trade_count = len(self.trades)

        for trade in self.trades:
            if trade.direction == Direction.LONG:
                pos_change = trade.volume
            else:
                pos_change = -trade.volume

            turnover = trade.price * trade.volume * size

            self.trading_pnl += pos_change * \
                (self.close_price - trade.price) * size
            self.end_pos += pos_change
            self.turnover += turnover
            self.commission += turnover * rate
            self.slippage += trade.volume * size * slippage

        # Net pnl takes account of commission and slippage cost
        self.total_pnl = self.trading_pnl + self.holding_pnl
        self.net_pnl = self.total_pnl - self.commission - self.slippage
```
&nbsp;



###  statistical indicators calculated strategy 
calculate_statistics function is based on mark-to-market profits and losses （DateFrame format ） to calculate the derivative index ， such as maximum retracement ,  annualized earnings ,  profit and loss ratio ,  sharpe ratio, etc. . 

```
            df["balance"] = df["net_pnl"].cumsum() + self.capital
            df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
            df["highlevel"] = (
                df["balance"].rolling(
                    min_periods=1, window=len(df), center=False).max()
            )
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # Calculate statistics value
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days = len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = total_trade_count / total_days

            total_return = (end_balance / self.capital - 1) * 100
            annual_return = total_return / total_days * 240
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            if return_std:
                sharpe_ratio = daily_return / return_std * np.sqrt(240)
            else:
                sharpe_ratio = 0
```
&nbsp;

###  statistical indicators mapping 
 by matplotlib draw 4 figures ：
-  funding plot 
-  drawdown map 
-  daily profit and loss chart 
-  daily profit and loss distribution 

```
    def show_chart(self, df: DataFrame = None):
        """"""
        if not df:
            df = self.daily_df
        
        if df is None:
            return

        plt.figure(figsize=(10, 16))

        balance_plot = plt.subplot(4, 1, 1)
        balance_plot.set_title("Balance")
        df["balance"].plot(legend=True)

        drawdown_plot = plt.subplot(4, 1, 2)
        drawdown_plot.set_title("Drawdown")
        drawdown_plot.fill_between(range(len(df)), df["drawdown"].values)

        pnl_plot = plt.subplot(4, 1, 3)
        pnl_plot.set_title("Daily Pnl")
        df["net_pnl"].plot(kind="bar", legend=False, grid=False, xticks=[])

        distribution_plot = plt.subplot(4, 1, 4)
        distribution_plot.set_title("Daily Pnl Distribution")
        df["net_pnl"].hist(bins=50)

        plt.show()
```

&nbsp;

###  single strategy backtesting example 

-  import and backtesting engine CTA tactics 
-  back to measured parameters ， such as ： variety , K line cycle ,  start and end dates backtesting ,  fees ,  slippage ,  contract size ,  seed money 
-  loading policies and data to the engine ， running back-tested . 
-  calculated based on the daily statistics profitability ， calculation of statistical indicators ， statistical indicators mapping . 


```
from vnpy.app.cta_strategy.backtesting import BacktestingEngine
from vnpy.app.cta_strategy.strategies.boll_channel_strategy import (
    BollChannelStrategy,
)
from datetime import datetime

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="IF88.CFFEX",
    interval="1m",
    start=datetime(2018, 1, 1),
    end=datetime(2019, 1, 1),
    rate=3.0/10000,
    slippage=0.2,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
)

engine.add_strategy(AtrRsiStrategy, {})
engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()
```

&nbsp;

###  portfolio backtesting example 

 portfolio backtesting backtesting is based on a single strategy ， the key is that each strategy corresponds with their BacktestingEngine objects ， here are the specific process ：

-  create a back-test function run_backtesting()， such a policy is created for each add their BacktestingEngine objects . 
```
from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
from vnpy.app.cta_strategy.strategies.atr_rsi_strategy import AtrRsiStrategy
from vnpy.app.cta_strategy.strategies.boll_channel_strategy import BollChannelStrategy
from datetime import datetime

def run_backtesting(strategy_class, setting, vt_symbol, interval, start, end, rate, slippage, size, pricetick, capital):
    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol=vt_symbol,
        interval=interval,
        start=start,
        end=end,
        rate=rate,
        slippage=slippage,
        size=size,
        pricetick=pricetick,
        capital=capital    
    )
    engine.add_strategy(strategy_class, setting)
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    return df
```

&nbsp;

-  they were single strategy backtesting ， get their DataFrame，( that DataFrame it includes trading hours ,  this warehouse ,  yesterday warehouse ,  fees ,  slippage ,  day net profit and loss ,  basic information such as the amount of net profit and loss ， but does not include the largest retracement ， sharpe ratio and other statistical information ), then DataFrame added and removed after the null value obtained portfolio DataFrame. 

```
df1 = run_backtesting(
    strategy_class=AtrRsiStrategy, 
    setting={}, 
    vt_symbol="IF88.CFFEX",
    interval="1m", 
    start=datetime(2019, 1, 1), 
    end=datetime(2019, 4, 30),
    rate=0.3/10000,
    slippage=0.2,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
    )

df2 = run_backtesting(
    strategy_class=BollChannelStrategy, 
    setting={'fixed_size': 16}, 
    vt_symbol="RB88.SHFE",
    interval="1m", 
    start=datetime(2019, 1, 1), 
    end=datetime(2019, 4, 30),
    rate=1/10000,
    slippage=1,
    size=10,
    pricetick=1,
    capital=1_000_000,
    )

dfp = df1 + df2
dfp =dfp.dropna() 
```

&nbsp;


-  create show_portafolio() function ， it is also creating a new BacktestingEngine objects ， incoming DataFrame calculation of statistical indicators such as the sharpe ratio, etc. ， and drawing .  so the function can not only display a single strategy backtesting results ， also can show portfolio backtesting results . 
```
def show_portafolio(df):
    engine = BacktestingEngine()
    engine.calculate_statistics(df)
    engine.show_chart(df)

show_portafolio(dfp)
```

&nbsp;

##  parameter optimization 
 parameter optimization module consists 3 constitute part ：

###  parameter settings 

-  set the interval parameter optimization ： such as boll_window set to start value 18， termination value 24， stepping into 2， this has been [18, 20, 22, 24]  this 4 the two parameters to be optimized . 
-  setting the target field optimization ： the sharpe ratio ,  profit and loss ratio ,  the total rate of return, etc. . 
-  combination of randomly generated parameter ： using an iterative tool to generate parameter combinations ， the composition is then packed into a parameter list consisting of a dictionaries 

```
class OptimizationSetting:
    """
    Setting for runnning optimization.
    """

    def __init__(self):
        """"""
        self.params = {}
        self.target_name = ""

    def add_parameter(
        self, name: str, start: float, end: float = None, step: float = None
    ):
        """"""
        if not end and not step:
            self.params[name] = [start]
            return

        if start >= end:
            print(" parameter optimization must be less than the starting point of the end point ")
            return

        if step <= 0:
            print(" parameter optimization step must be greater than 0")
            return

        value = start
        value_list = []

        while value <= end:
            value_list.append(value)
            value += step

        self.params[name] = value_list

    def set_target(self, target_name: str):
        """"""
        self.target_name = target_name

    def generate_setting(self):
        """"""
        keys = self.params.keys()
        values = self.params.values()
        products = list(product(*values))

        settings = []
        for p in products:
            setting = dict(zip(keys, p))
            settings.append(setting)

        return settings
```

&nbsp;

###  parameter combination backtesting 

 when multi-process optimization ， each process runs optimize function ， the results of the composition and the output parameter optimization target field .  it comprises the following steps ：
-  call backtesting engine 
-  backtesting input settings 
-  input parameters for the combination to the policy 
-  running back-tested 
-  return back test results ， include ： parameter combination ,  objective optimization field values ,  strategy statistical indicators 

```
def optimize(
    target_name: str,
    strategy_class: CtaTemplate,
    setting: dict,
    vt_symbol: str,
    interval: Interval,
    start: datetime,
    rate: float,
    slippage: float,
    size: float,
    pricetick: float,
    capital: int,
    end: datetime,
    mode: BacktestingMode,
):
    """
    Function for running in multiprocessing.pool
    """
    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol=vt_symbol,
        interval=interval,
        start=start,
        rate=rate,
        slippage=slippage,
        size=size,
        pricetick=pricetick,
        capital=capital,
        end=end,
        mode=mode
    )

    engine.add_strategy(strategy_class, setting)
    engine.load_data()
    engine.run_backtesting()
    engine.calculate_result()
    statistics = engine.calculate_statistics()

    target_value = statistics[target_name]
    return (str(setting), target_value, statistics)
```

&nbsp;

###  multi-process optimization 

-  according to CPU the audit process to create ： if the CPU for 4 nuclear ， create 4 a process 
-  we are called in each process apply_async( ) the method combination of operating parameters for backtesting ， adding to its backtesting results results in  （apply_async asynchronous non-blocking ， that is, without waiting for the current process is finished ， at any time to carry out the process of switching system according to schedule . ）
- pool.close() versus pool.join() after finish the task for process ， close to process . 
-  correct results the contents are sorted by optimizing field goal standard ， output . 

```
        pool = multiprocessing.Pool(multiprocessing.cpu_count())

        results = []
        for setting in settings:
            result = (pool.apply_async(optimize, (
                target_name,
                self.strategy_class,
                setting,
                self.vt_symbol,
                self.interval,
                self.start,
                self.rate,
                self.slippage,
                self.size,
                self.pricetick,
                self.capital,
                self.end,
                self.mode
            )))
            results.append(result)

        pool.close()
        pool.join()

        # Sort results and output
        result_values = [result.get() for result in results]
        result_values.sort(reverse=True, key=lambda result: result[1])

        for value in result_values:
            msg = f" parameter ：{value[0]},  aims ：{value[1]}"
            self.output(msg)

        return result_values
```

&nbsp;

##  firm run 
 in the firm environment ， users can write good basis CTA strategy to create a new instance ， a key to initialize ,  start up ,  stop strategy . 


###  create a policy instance 
 users can write good basis CTA strategy to create a new instance ， examples of the benefits of the policy is that the same strategy can go to contract simultaneously run multiple varieties ， and the parameters may be different for each instance of . 
 when creating an instance of the need to fill the instance name figure ,  variety contract ,  parameter settings .  note ： the instance name must be unique ； contract name is vt_symbol the format ， such as IF1905.CFFEX. 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_strategy/add_strategy.png)

 create a policy process is as follows ：
-  examples of the same name check policy 
-  adding policy configuration information (strategy_name, vt_symbol, setting) to strategies dictionary 
-  to subscribe to add the policy to contract information quotes symbol_strategy_map dictionary ；
-  save the policy configuration information to json the paper ；
-  in the graphical interface to update status information . 

```
    def add_strategy(
        self, class_name: str, strategy_name: str, vt_symbol: str, setting: dict
    ):
        """
        Add a new strategy.
        """
        if strategy_name in self.strategies:
            self.write_log(f" create a policy failure ， the presence of the same name {strategy_name}")
            return

        strategy_class = self.classes[class_name]

        strategy = strategy_class(self, strategy_name, vt_symbol, setting)
        self.strategies[strategy_name] = strategy

        # Add vt_symbol to strategy map.
        strategies = self.symbol_strategy_map[vt_symbol]
        strategies.append(strategy)

        # Update to setting file.
        self.update_strategy_setting(strategy_name, setting)

        self.put_strategy_event(strategy)
```

&nbsp;

###  initialization policy 
-  call the strategy of class on_init() callback , and load historical data ；
-  recovery strategy state before the last exit ；
-  from .vntrader/cta_strategy_data.json read within policy parameters ， the latest technology indicators ， and the number of positions ；
-  call interface subcribe() subscribe function specified market information ；
-  strategy becomes initialized state True， and updates to the log . 
  
```
    def _init_strategy(self):
        """
        Init strategies in queue.
        """
        while not self.init_queue.empty():
            strategy_name = self.init_queue.get()
            strategy = self.strategies[strategy_name]

            if strategy.inited:
                self.write_log(f"{strategy_name} initialization has been completed ， repeat ban ")
                continue

            self.write_log(f"{strategy_name} begin initialization ")

            # Call on_init function of strategy
            self.call_strategy_func(strategy, strategy.on_init)

            # Restore strategy data(variables)
            data = self.strategy_data.get(strategy_name, None)
            if data:
                for name in strategy.variables:
                    value = data.get(name, None)
                    if value:
                        setattr(strategy, name, value)

            # Subscribe market data
            contract = self.main_engine.get_contract(strategy.vt_symbol)
            if contract:
                req = SubscribeRequest(
                    symbol=contract.symbol, exchange=contract.exchange)
                self.main_engine.subscribe(req, contract.gateway_name)
            else:
                self.write_log(f" subscribe to market failure ， can not find contract {strategy.vt_symbol}", strategy)

            # Put event to update init completed status.
            strategy.inited = True
            self.put_strategy_event(strategy)
            self.write_log(f"{strategy_name} loading finished ")
        
        self.init_thread = None
```

&nbsp;

###  start policy 
-  check the initialization state policy ；
-  check the startup state strategy ， avoid duplication start ；
-  call the strategy of class on_start() function to start policies ；
-  policy startup status changes True， and updates to the graphical interface . 

```
    def start_strategy(self, strategy_name: str):
        """
        Start a strategy.
        """
        strategy = self.strategies[strategy_name]
        if not strategy.inited:
            self.write_log(f" tactics {strategy.strategy_name} startup failed ， please initialization ")
            return

        if strategy.trading:
            self.write_log(f"{strategy_name} has been launched ， do not repeat ")
            return

        self.call_strategy_func(strategy, strategy.on_start)
        strategy.trading = True

        self.put_strategy_event(strategy)
```

&nbsp;

###  stop strategy 
-  check the startup state strategy ；
-  call the strategy of class on_stop() function stops policy ；
-  update policy startup state False；
-  all transactions for the commission （ market order / limit order / local stop single ） operation carried out withdrawals ；
-  the policy parameters ， the latest technology indicators ， and the number of positions to save .vntrader/cta_strategy_data.json inside ；
-  in the graphical interface status update policy . 

```
    def stop_strategy(self, strategy_name: str):
        """
        Stop a strategy.
        """
        strategy = self.strategies[strategy_name]
        if not strategy.trading:
            return

        # Call on_stop function of the strategy
        self.call_strategy_func(strategy, strategy.on_stop)

        # Change trading status of strategy to False
        strategy.trading = False

        # Cancel all orders of the strategy
        self.cancel_all(strategy)

        # Sync strategy variables to data file
        self.sync_strategy_data(strategy)

        # Update GUI
        self.put_strategy_event(strategy)
```

&nbsp;

###  edit policy 
-  reconfigure policy parameters dictionary setting；
-  updates to the policy parameters dictionary ；
-  in the graphical interface status update policy . 

```
    def edit_strategy(self, strategy_name: str, setting: dict):
        """
        Edit parameters of a strategy.
        """
        strategy = self.strategies[strategy_name]
        strategy.update_setting(setting)

        self.update_strategy_setting(strategy_name, setting)
        self.put_strategy_event(strategy)
```

&nbsp;

###  removal policy 
-  check the policy status ， only stop strategy can be removed from the policy ；
-  from json removal policy configuration file (strategy_name, vt_symbol, setting)；
-  from symbol_strategy_map dictionary to remove the policy contract subscription information ；
-  from strategy_orderid_map dictionary removing activity delegates record ；
-  from strategies dictionary remove the configuration information for the policy . 

```
    def remove_strategy(self, strategy_name: str):
        """
        Remove a strategy.
        """
        strategy = self.strategies[strategy_name]
        if strategy.trading:
            self.write_log(f" tactics {strategy.strategy_name} removal failed ， please stop ")
            return

        # Remove setting
        self.remove_strategy_setting(strategy_name)

        # Remove from symbol strategy map
        strategies = self.symbol_strategy_map[strategy.vt_symbol]
        strategies.remove(strategy)

        # Remove from active orderid map
        if strategy_name in self.strategy_orderid_map:
            vt_orderids = self.strategy_orderid_map.pop(strategy_name)

            # Remove vt_orderid strategy map
            for vt_orderid in vt_orderids:
                if vt_orderid in self.orderid_strategy_map:
                    self.orderid_strategy_map.pop(vt_orderid)

        # Remove from strategies
        self.strategies.pop(strategy_name)

        return True
```

&nbsp;

###  lock operation 

 users in the preparation of policy ， you can fill lock fields to make the policy complete lock operation ， that is now prohibited flat ， instead reverse open . 

-  in cta policy template template in ， we can see the following specific functions have commissioned lock field ， and defaults False. 

```
    def buy(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        Send buy order to open a long position.
        """
        return self.send_order(Direction.LONG, Offset.OPEN, price, volume, stop, lock)

    def sell(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        Send sell order to close a long position.
        """
        return self.send_order(Direction.SHORT, Offset.CLOSE, price, volume, stop, lock)

    def short(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        Send short order to open as short position.
        """
        return self.send_order(Direction.SHORT, Offset.OPEN, price, volume, stop, lock)

    def cover(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        Send cover order to close a short position.
        """
        return self.send_order(Direction.LONG, Offset.CLOSE, price, volume, stop, lock)

    def send_order(
        self,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False
    ):
        """
        Send a new order.
        """
        if self.trading:
            vt_orderids = self.cta_engine.send_order(
                self, direction, offset, price, volume, stop, lock
            )
            return vt_orderids
        else:
            return []
```

&nbsp;

-  set up lock=True rear ，cta firm engine send_order() function generator response ， and it calls its most fundamental functions entrusted send_server_order() lock commission to deal with the conversion .  the first is to create the original commission original_req， then call converter file inside OffsetConverter category convert_order_request related to conversion . 

```
    def send_order(
        self,
        strategy: CtaTemplate,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        stop: bool,
        lock: bool
    ):
        """
        """
        contract = self.main_engine.get_contract(strategy.vt_symbol)
        if not contract:
            self.write_log(f" commissioned failure ， can not find contract ：{strategy.vt_symbol}", strategy)
            return ""

        if stop:
            if contract.stop_supported:
                return self.send_server_stop_order(strategy, contract, direction, offset, price, volume, lock)
            else:
                return self.send_local_stop_order(strategy, direction, offset, price, volume, lock)
        else:
            return self.send_limit_order(strategy, contract, direction, offset, price, volume, lock)

    def send_limit_order(
        self,
        strategy: CtaTemplate,
        contract: ContractData,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        lock: bool
    ):
        """
        Send a limit order to server.
        """
        return self.send_server_order(
            strategy,
            contract,
            direction,
            offset,
            price,
            volume,
            OrderType.LIMIT,
            lock
        )

    def send_server_order(
        self,
        strategy: CtaTemplate,
        contract: ContractData,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        type: OrderType,
        lock: bool
    ):
        """
        Send a new order to server.
        """
        # Create request and send order.
        original_req = OrderRequest(
            symbol=contract.symbol,
            exchange=contract.exchange,
            direction=direction,
            offset=offset,
            type=type,
            price=price,
            volume=volume,
        )

        # Convert with offset converter
        req_list = self.offset_converter.convert_order_request(original_req, lock)

        # Send Orders
        vt_orderids = []

        for req in req_list:
            vt_orderid = self.main_engine.send_order(
                req, contract.gateway_name)
            vt_orderids.append(vt_orderid)

            self.offset_converter.update_order_request(req, vt_orderid)
            
            # Save relationship between orderid and strategy.
            self.orderid_strategy_map[vt_orderid] = strategy
            self.strategy_orderid_map[strategy.strategy_name].add(vt_orderid)

        return vt_orderids        
```

&nbsp;

-  in convert_order_request_lock() function ， calculating an amount of the first cartridge and this amount may be yesterday ； then analyzing ： if this warehouse ， open only （ lock ）； no this position when ， if the amount is smaller than yesterday closing available ， all flat yesterday ， on the contrary ， first flat yesterday ， the remaining reverse open . 

```
    def convert_order_request_lock(self, req: OrderRequest):
        """"""
        if req.direction == Direction.LONG:
            td_volume = self.short_td
            yd_available = self.short_yd - self.short_yd_frozen
        else:
            td_volume = self.long_td
            yd_available = self.long_yd - self.long_yd_frozen

        # If there is td_volume, we can only lock position
        if td_volume:
            req_open = copy(req)
            req_open.offset = Offset.OPEN
            return [req_open]
        # If no td_volume, we close opposite yd position first
        # then open new position
        else:
            open_volume = max(0,  req.volume - yd_available)
            req_list = []

            if yd_available:
                req_yd = copy(req)
                if self.exchange == Exchange.SHFE:
                    req_yd.offset = Offset.CLOSEYESTERDAY
                else:
                    req_yd.offset = Offset.CLOSE
                req_list.append(req_yd)

            if open_volume:
                req_open = copy(req)
                req_open.offset = Offset.OPEN
                req_open.volume = open_volume
                req_list.append(req_open)

            return req_list

```
