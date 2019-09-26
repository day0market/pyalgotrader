# CTAPolicy Module


## Modules

CTAMainly by the strategy module7Constitute part, As shown below：

- base：DefinedCTAModule used in some of the basic settings, Such as engine type（Backtesting/Firm）、Back to the measurement mode（Kline/Tick）、Local single stop and a stop order status definitions（Waiting/Revoked/Triggered）. 
  
- template：DefinedCTAPolicy Template（It includes signal generation and delegate management）、CTAsignal（It is only responsible for signal generation）、Target position algorithm（Only responsible for delegated administration, It applies to split the giant commission, Reduce the cost impact）. 
- strategies: The official providedctaPolicy Example, It contains double the average from the most basic strategy, To channel breakout type of strategy Bollinger Bands, To cross time cycle strategy, Then the signal generation and delegated administration open to independent multi-signal strategy. (User-defined strategy can be placedstrategiesFolder run)
- backesting：It includes backtesting engine and parameter optimization. Backtesting engine which defines the data load、Commissioned matching mechanism、Calculation and statistical indicators related to profitability、Results plotting other functions. 
- converter：It defines this level for the period of the species/Flat commission mode conversion module yesterday；For users of other species can also optional parameterslockLock mode switch to. 
- engine：DefinedCTAStrategy firm engine, These include：RQDataThe client initialization and loading data、Strategies and start initialization、PushTickSubscribe to the strategy market、Hanging cancellation operation、Strategies such as stop and remove. 
- ui：based onPyQt5ofGUIGraphics applications. 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_strategy/seix_elementos.png "enter image title here")

&nbsp;

## Loading

In the real dish, RQDataInitialized strategy through real-time load data. The main function inCTAFirm engineengine.pyIn the realization. 
Here are the specific process：
- In the menu bar click“Configuration”, Enter the global configuration page inputRQDataaccount password；Or direct configurationjsonfile, That is under the user's directory.vntraderFolders foundvt_setting.json, Figure. 
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_strategy/RQData_setting.png "enter image title here")

- initializationRQDataClient：Fromvt_setting.jsonReadRQDataAccount、Password torq_client.init()Function initializes

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


- RQDataLoading data firm：Entryvt_symbolRear, First in line will be converted toRQDataFormatsrq_symbol, byget_price()Download data function, And inserted into the database. 
  
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

## Strategy Development
CTA Strategy templates provide a complete signal generation and delegate management functions, Users can develop their own strategies based on the template. The new strategy can be placed in the user runs the file（recommend）, As inc:\users\administrator.vntraderCreate a directorystrategiesfolder；It can be placed in the root directoryvnpy\app\cta_strategy\strategiesFolder. 
note：Strategy file is named underline mode, Such as boll_channel_strategy.py；The strategy class name is used in camel, Such as BollChannelStrategy. 

By the following BollChannelStrategyPolicy example, concrete steps to demonstrate the development strategy：

### parameter settings

Define strategy parameters and strategy variables initialized. strategy parameters for the class strategy of public property, Users can call or change strategy parameters by creating a new instance. 

As forrb1905Variety, Users can create based onBollChannelStrategyExamples of strategies, Such as RB_BollChannelStrategy, boll_window it can be made 18 Change 30. 

Examples of ways to create strategies to effectively implement a strategy to run a number of varieties, strategy parameters and which can be adjusted by the features of species. 
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

### Initialization class
Initialization points3step：
- bysuper( )The methods are inheritedCTAPolicy Template, in__init__( )Incoming functionCTAengine、strategy Name、vt_symbol、parameter settings. 
- transferKLine generation module:By the time slicesTickData synthesis1minuteKLine data, Then a larger time period data, Such as15minuteKline. 
- transferKLine time sequence manager module：based onKLine data, Such as1minute、15minute, To form the corresponding technical specifications. 
  
```
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(BollChannelStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )

        self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am = ArrayManager()
```

### Initialization strategy、start up、stop
by “CTATactics” Button component-related functions to achieve. 

note：functionload_bar(10), On behalf of the strategy needs to load initialization10Trading historical data. The historical data can beTickdata, can also beKLine data. In the initialization time strategy, Will callKCalculating line time sequence manager and cache related calculation index, But the transaction does not trigger. 

```
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("Strategy initialization")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("strategy startup")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("Stop strategy")
```
### TickData Return
Subscribe to a variety of tactics contract market, Exchange will pushTickThe data on strategy. 

due to BollChannelStrategy is based on15minuteKGenerating a signal line transactions, It is receivedTickAfter data, Need to useKLine generation module inside update_tick function, By a method of time-slicing, Polymerized into1minuteKLine data, And push on_bar function. 

```
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)
```

### KLine data return

Receive push over1minuteKAfter the data line, byKLine generation module insideupdate_barfunction, The method of minutes to slice, synthesis15minuteKLine data, And pushon_15min_barfunction. 
```
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)
```

### 15minuteKLine data return

Be responsible forCTAGenerating a signal, by3Parts：
- Clear Unsold commissioned：In order to prevent under the list before a15Minutes no deal, But next15Minutes may have adjusted the price, then applycancel_all()Unsold method previously withdrawn all at once commissioned, This is to ensure that the current strategy15The entire state of minutes and only began to be clear. 
- transferKLine time sequence manager module：Based on the latest15minuteKCalculating respective line data calculation index, The vertical rail Bollinger band channel、CCIindex、ATRindex
- Signal calculation：And by determining the binding positionsCCIindex、Bollinger band channel、ATRIndicators point to hang out in the channel breakout single delegate stop（buy/sell), At the same time set the departure point(short/cover). 

note：CTAStrategy with specific low and high winning percentage than the profit and loss：In the case of difficult to improve the odds of, Research strategies to enhance profit and loss ratio in favor of increased profitability strategy. 

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

### Return commission、Return on turnover、One-stop return

In the strategy can be directly pass, The specific application logic to back-test/Firm responsible for engine. 
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

## Research measured back
backtesting.py it defines the backtesting engine, The following describes the functions related functions, Backtesting engine and application examples：

### Loading strategy

TheCTAPolicy logic, The corresponding contract Variety, And parameter settings（Can be modified outside the strategy file）Loaded into the back-tested engine. 
```
    def add_strategy(self, strategy_class: type, setting: dict):
        """"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self, strategy_class.__name__, self.vt_symbol, setting
        )
```
&nbsp;

### Loading Historical Data

Responsible for loading historical data corresponding to species, roughly has4Steps：
- The different data types, DividedKWire mode andTickmode；
- byselect().where()method, Conditionally select data from the database, Which includes screening criteria：vt_symbol、 Backtesting Start Date、Backtesting end date、KLine cycle（KOffline Mode）；
- order_by(DbBarData.datetime)It represents the data to be loaded chronologically；
- Loading data is carried out in an iterative manner, The final data is storedself.history_data. 

```
    def load_data(self):
        """"""
        self.output("Begins loading historical data")

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

        self.output(f"Historical data loaded, The amount of data：{len(self.history_data)}")
```
&nbsp;

### Brokered transactions

Loading CTA after strategies and relevant historical data, Strategy related indicators will be calculated according to the latest data. If they meet the conditions will generate trading signals, Issued a specific commission（buy/sell/short/cover）, And the next oneKLine auction. 

Depending on the type of delegate, Backtesting engine provides2Brokered transactions kinds of mechanisms to try to imitate the real trade links：

- Limit orders brokered transactions：（Direction, for example to buy）First determine whether the transaction occurred, Standard price for the transaction commission>= Under aKThe lowest line；Then determine the transaction price, Price and the transaction price was commissioned at aKMinimum line opening price. 

- Stop single brokered transactions：（Direction, for example to buy）First determine whether the transaction occurred, Standard price for the transaction commission<= Under aKThe highest price line；Then determine the transaction price, Price and the transaction price was commissioned at aKMaximum line opening price. 

&nbsp;

The following shows the engine limit orders brokered transactions process：
- Brokered transactions will determine the price；
- All limit order limit order traversal dictionary, Push commissioned into the transaction queue status is not updated；
- Analyzing Transaction Status, If there is turnover, Push transaction data and commission data；
- Delete turnover limit orders from the dictionary. 

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

### Profit and loss calculation method

Based on the closing price、Day positions、Contract size、Slippage、Calculate the total commission rate gains and losses and net gains and losses, And the calculation resultDataFrameOutput format, Complete statistics based on mark-to-market gains and losses. 

The following shows the calculation of profit and loss

- Floating profit and loss = Positions \*（Closing price - Yesterday's closing price）\*  Contract size
- The actual profit and loss = The amount of change positions  \* （At that time the closing price - Open price）\* Contract size
- Total profit and loss = Floating profit and loss + The actual profit and loss
- Net profit and loss = Total profit and loss - Total fee - The total slippage

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



### Statistical indicators calculated strategy
calculate_statisticsFunction is based on mark-to-market profits and losses（DateFrameformat）To calculate the derivative index, Such as maximum retracement、Annualized earnings、Profit and loss ratio、Sharpe ratio, etc.. 

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

### Statistical Indicators Mapping
by matplotlib draw 4 Figures：
- Funding plot
- Drawdown map
- Daily profit and loss chart
- Daily profit and loss distribution

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

### Single Strategy Backtesting example

- Import and backtesting engineCTATactics
- Back to measured parameters, Such as：Variety、KLine cycle、Start and end dates backtesting、Fees、Slippage、Contract size、Seed money
- Loading policies and data to the engine, Running back-tested. 
- Calculated based on the daily statistics profitability, Calculation of statistical indicators, Statistical Indicators Mapping. 


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

### Portfolio backtesting example

Portfolio Backtesting Backtesting is based on a single strategy, The key is that each strategy corresponds with theirBacktestingEngineObjects, Here are the specific process：

- Create a back-test function run_backtesting(), Such a strategy is created for each add theirBacktestingEngineObjects. 
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

- They were single strategy backtesting, Get their DataFrame, (ThatDataFrameIt includes trading hours、This warehouse、Yesterday warehouse、Fees、Slippage、Day net profit and loss、Basic information such as the amount of net profit and loss, But does not include the largest retracement, Sharpe ratio and other statistical information),ThenDataFrameAdded and removed after the null value obtained portfolioDataFrame. 

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


- createshow_portafolio() function, It is also creating a new BacktestingEngineObjects, IncomingDataFrameCalculation of statistical indicators such as the Sharpe ratio, etc., And drawing. So the function can not only display a single strategy backtesting results, Also can show portfolio backtesting results. 
```
def show_portafolio(df):
    engine = BacktestingEngine()
    engine.calculate_statistics(df)
    engine.show_chart(df)

show_portafolio(dfp)
```

&nbsp;

## Parameter optimization
Parameter optimization module consists3Constitute part：

### parameter settings

- Set the interval parameter optimization：Such asboll_windowSet to start value18, Termination value24, Stepping into2, This has been[18, 20, 22, 24] This4The two parameters to be optimized. 
- Set the optimization target field：The Sharpe ratio、Profit and loss ratio、The total rate of return, etc.. 
- Combination of randomly generated parameter：Using an iterative tool to generate parameter combinations, The composition is then packed into a parameter list consisting of a dictionaries

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
            print("Parameter optimization must be less than the starting point of the end point")
            return

        if step <= 0:
            print("Parameter optimization step must be greater than0")
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

### Parameter combination backtesting

When multi-process optimization, Each process runsoptimizefunction, The results of the composition and the output parameter optimization target field. It comprises the following steps：
- Call backtesting engine
- Backtesting input settings
- Input parameters for the combination to the strategy
- Running back-tested
- Return back test results, include：Parameter combination、Objective optimization field values、Strategy statistical indicators

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

### Multi-process optimization

- according toCPUThe audit process to create：If theCPUfor4nuclear, Create4A process
- We are called in each process apply_async( )The method combination of operating parameters for backtesting, Adding to its backtesting resultsresultsin （apply_asyncAsynchronous non-blocking, That is, without waiting for the current process is finished, At any time to carry out the process of switching system according to schedule. ）
- pool.close() versus pool.join() After finish the task for process, Close to process. 
- Correct results the contents are sorted by optimizing field goal standard, Output. 

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
            msg = f"parameter：{value[0]}, aims：{value[1]}"
            self.output(msg)

        return result_values
```

&nbsp;

## Firm run
In the firm environment, Users can write good basis CTAStrategy to create a new instance, A key to initialize、start up、Stop Strategy. 


### Create a strategy instance
Users can write good basis CTAStrategy to create a new instance, Examples of the benefits of the strategy is that the same strategy can go to contract simultaneously run multiple varieties, And the parameters may be different for each instance of. 
When creating an instance of the need to fill the instance name Figure、Variety contract、parameter settings. note：The instance name must be unique；Contract name isvt_symbolThe format, Such asIF1905.CFFEX. 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_strategy/add_strategy.png)

Create a strategy process is as follows：
- Examples of the same name Check strategy
- Adding strategy configuration information(strategy_name, vt_symbol, setting)TostrategiesDictionary
- To subscribe to add the strategy to contract information Quotessymbol_strategy_mapDictionary；
- Save the strategy configuration information tojsonThe paper；
- In the graphical interface to update status information. 

```
    def add_strategy(
        self, class_name: str, strategy_name: str, vt_symbol: str, setting: dict
    ):
        """
        Add a new strategy.
        """
        if strategy_name in self.strategies:
            self.write_log(f"Create a strategy failure, The presence of the same name{strategy_name}")
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

### Initialization strategy
- Call the strategy of classon_init()Callback,And load historical data；
- Recovery strategy state before the last exit；
- From.vntrader/cta_strategy_data.jsonRead within strategy parameters, The latest technology indicators, And the number of positions；
- Call interfacesubcribe()Subscribe function specified market information；
- Strategy becomes initialized stateTrue, And updates to the log. 
  
```
    def _init_strategy(self):
        """
        Init strategies in queue.
        """
        while not self.init_queue.empty():
            strategy_name = self.init_queue.get()
            strategy = self.strategies[strategy_name]

            if strategy.inited:
                self.write_log(f"{strategy_name}Initialization has been completed, Repeat ban")
                continue

            self.write_log(f"{strategy_name}Begin initialization")

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
                self.write_log(f"Subscribe to market failure, Can not find contract{strategy.vt_symbol}", strategy)

            # Put event to update init completed status.
            strategy.inited = True
            self.put_strategy_event(strategy)
            self.write_log(f"{strategy_name}loading finished")
        
        self.init_thread = None
```

&nbsp;

### Start strategy
- Check the initialization state strategy；
- Check the startup state strategy, Avoid duplication start；
- Call the strategy of classon_start()Function to start policies；
- strategy startup status changesTrue, And updates to the graphical interface. 

```
    def start_strategy(self, strategy_name: str):
        """
        Start a strategy.
        """
        strategy = self.strategies[strategy_name]
        if not strategy.inited:
            self.write_log(f"Tactics{strategy.strategy_name}Startup failed, Please initialization")
            return

        if strategy.trading:
            self.write_log(f"{strategy_name}Has been launched, Do not Repeat")
            return

        self.call_strategy_func(strategy, strategy.on_start)
        strategy.trading = True

        self.put_strategy_event(strategy)
```

&nbsp;

### Stop Strategy
- Check the startup state strategy；
- Call the strategy of classon_stop()Function stops strategy；
- Update strategy startup stateFalse；
- All transactions for the commission（Market Order/Limit Order/Local stop single）Operation carried out withdrawals；
- The strategy parameters, The latest technology indicators, And the number of positions to save.vntrader/cta_strategy_data.jsonInside；
- In the graphical interface status update strategy. 

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

### Edit strategy
- Reconfigure strategy parameters dictionarysetting；
- Updates to the strategy parameters dictionary；
- In the graphical interface status update strategy. 

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

### Removal strategy
- Check the strategy status, Only stop strategy can be removed from the strategy；
- From jsonRemoval strategy configuration file(strategy_name, vt_symbol, setting)；
- From symbol_strategy_mapDictionary to remove the strategy subscription contract information；
- From strategy_orderid_mapDictionary removing activity delegates Record；
- From strategiesDictionary remove the configuration information for the strategy. 

```
    def remove_strategy(self, strategy_name: str):
        """
        Remove a strategy.
        """
        strategy = self.strategies[strategy_name]
        if strategy.trading:
            self.write_log(f"Tactics{strategy.strategy_name}Removal failed, Please stop")
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

### Lock operation

Users in the preparation of strategy, You can fill lockFields to make the strategy complete Lock operation, That is now prohibited flat, Instead reverse Open. 

- inctaPolicy Templatetemplatein, We can see the following specific functions have commissionedlockField, And defaultsFalse. 

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

- Set uplock=TrueRear, ctaFirm enginesend_order()Function generator response, And it calls its most fundamental functions entrustedsend_server_order()Lock commission to deal with the conversion. The first is to create the original commissionoriginal_req, Then callconverterFile insideOffsetConverterCategoryconvert_order_requestRelated to conversion. 

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
            self.write_log(f"Commissioned failure, Can not find contract：{strategy.vt_symbol}", strategy)
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

- inconvert_order_request_lock()Function, Calculating an amount of the first cartridge and this amount may be yesterday；Then Analyzing：If this warehouse, Open only（Lock）；No this position when, If the amount is smaller than yesterday closing available, All flat yesterday, on the contrary, First flat yesterday, The remaining reverse Open. 

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
