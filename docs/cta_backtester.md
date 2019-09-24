# CTABacktesting module
CTABacktesting module is based onPyQt5withpyqtgraphGraphical back-tested tool。start upVN TraderRear，In the menu bar“Features-> CTABacktesting”To enter the graphical interface backtesting，As shown below。CTABacktesting module mainly realizes3Function：Download historical market data、Strategy Backtesting、Parameter optimization、KLine chart point of sale display。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/cta_backtester.png)

&nbsp;

## Load Startup
Backtesting into the graphical interface“CTABacktesting”Rear，Initial work will be completed soon：Backtesting engine initialization、initializationRQDataClient。

```
    def init_engine(self):
        """"""
        self.write_log("initializationCTABacktesting engine")

        self.backtesting_engine = BacktestingEngine()
        # Redirect log from backtesting engine outside.
        self.backtesting_engine.output = self.write_log

        self.write_log("Policy file loaded")

        self.init_rqdata()

    def init_rqdata(self):
        """
        Init RQData client.
        """
        result = rqdata_client.init()
        if result:
            self.write_log("RQDataSuccessful initialization data interface")
```

&nbsp;


## Download Data
Before starting strategy backtesting，We must ensure that there is sufficient historical data in the database。ThereforevnpyIt provides a historical data download function keys。

### RQData
RQDataProvide domestic stock、ETF、Historical data of futures and options。
Its main function is to download data based onRQDataofget_price()Function to achieve。
```
get_price(
    order_book_ids, start_date='2013-01-04', end_date='2014-01-04',
    frequency='1d', fields=None, adjust_type='pre', skip_suspended =False,
    market='cn'
)
```


Before use to ensure thatRQDataInitialized，Then fill in the following4Field information：
- Native code：Variety contract format+Exchange，Such asIF88.CFFEX、rb88.SHFE；Then at the bottom byRqdataClientofto_rq_symbol()Function into line withRQDataformat，correspondRQDatainget_price()Functionorder_book_idsField。
- KLine cycle：You can fill1m、1h、d、w，correspondget_price()FunctionfrequencyField。
- start date：The formatyy/mm/dd，Such as2017/4/21，correspondget_price()Functionstart_dateField。（Click the window on the right arrow button to change the Date Size）
- End Date：The formatyy/mm/dd，Such as2019/4/22，correspondget_price()Functionend_dateField。（Click the window on the right arrow button to change the Date Size）
  
After filling out the information fields，Click below“Download Data”Button to start the download，Download the success shown in Fig.。


![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/data_loader.png)

&nbsp;

### IB

Interactive Brokers offers external disk stock、futures、Historical data option。
Before downloading must be connectedIBinterface，Because of its function is mainly based on download dataIbGatewayclassquery_history()Function to achieve。

```
    def query_history(self, req: HistoryRequest):
        """"""
        self.history_req = req

        self.reqid += 1

        ib_contract = Contract()
        ib_contract.conId = str(req.symbol)
        ib_contract.exchange = EXCHANGE_VT2IB[req.exchange]

        if req.end:
            end = req.end
            end_str = end.strftime("%Y%m%d %H:%M:%S")
        else:
            end = datetime.now()
            end_str = ""

        delta = end - req.start
        days = min(delta.days, 180)     # IB only provides 6-month data
        duration = f"{days} D"
        bar_size = INTERVAL_VT2IB[req.interval]

        if req.exchange == Exchange.IDEALPRO:
            bar_type = "MIDPOINT"
        else:
            bar_type = "TRADES"

        self.client.reqHistoricalData(
            self.reqid,
            ib_contract,
            end_str,
            duration,
            bar_size,
            bar_type,
            1,
            1,
            False,
            []
        )

        self.history_condition.acquire()    # Wait for async data return
        self.history_condition.wait()
        self.history_condition.release()

        history = self.history_buf
        self.history_buf = []       # Create new buffer list
        self.history_req = None

        return history
```
&nbsp;

### BITMEX

BITMEXCurrency Exchange provides digital historical data。
Due to differences in the simulation environment and market environment is big firm，Therefore you need to log in with a firm accountBIMEXInterface to download real market data，Its main function is to download data based onBitmexGatewayclassquery_history()Function to achieve。

```
    def query_history(self, req: HistoryRequest):
        """"""
        if not self.check_rate_limit():
            return

        history = []
        count = 750
        start_time = req.start.isoformat()

        while True:
            # Create query params
            params = {
                "binSize": INTERVAL_VT2BITMEX[req.interval],
                "symbol": req.symbol,
                "count": count,
                "startTime": start_time
            }

            # Add end time if specified
            if req.end:
                params["endTime"] = req.end.isoformat()

            # Get response from server
            resp = self.request(
                "GET",
                "/trade/bucketed",
                params=params
            )

            # Break if request failed with other status code
            if resp.status_code // 100 != 2:
                msg = f"Failure to obtain historical data，status code：{resp.status_code}，information：{resp.text}"
                self.gateway.write_log(msg)
                break
            else:
                data = resp.json()
                if not data:
                    msg = f"Obtain historical data is empty，Starting time：{start_time}，Quantity：{count}"
                    break

                for d in data:
                    dt = datetime.strptime(
                        d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    bar = BarData(
                        symbol=req.symbol,
                        exchange=req.exchange,
                        datetime=dt,
                        interval=req.interval,
                        volume=d["volume"],
                        open_price=d["open"],
                        high_price=d["high"],
                        low_price=d["low"],
                        close_price=d["close"],
                        gateway_name=self.gateway_name
                    )
                    history.append(bar)

                begin = data[0]["timestamp"]
                end = data[-1]["timestamp"]
                msg = f"Get historical success，{req.symbol} - {req.interval.value}，{begin} - {end}"
                self.gateway.write_log(msg)

                # Break if total data count less than 750 (latest date collected)
                if len(data) < 750:
                    break

                # Update start time
                start_time = bar.datetime + TIMEDELTA_MAP[req.interval]

        return history
```

&nbsp;

## Strategy Backtesting
After downloading historical data，Configure the following fields：Trading straregy、Fee rate、Trading Slippage、Contract Multiplier、Price beat、Backtesting funds。
These fields correspond to majorBacktesterEngineCategoryrun_backtestingfunction。

If the historical data already exists in the database，Without re-downloading，Import data directly from the local database back the measured。note，vt_symbolThe item code format.In the form of exchange of，Such asIF1908.CFFEX，Import will automatically be divided into two types and exchanges

```
def run_backtesting(
    self, class_name: str, vt_symbol: str, interval: str, start: datetime, 
    end: datetime, rate: float, slippage: float, size: int, pricetick: float, 
    capital: int, setting: dict
)：
```


Click below“Start backtesting”Button to start backtesting：
First, the parameters window will pop up as shown in FIG.，For adjusting the policy parameters。This setting corresponds to therun_backtesting()Functionsettingdictionary。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/parameter_setting.png)



Click on“confirm”Button starts running back to test，At the same time the log information interface will output，Figure。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/backtesting_log.png)

Statistics chart will show back-tested after completion。

&nbsp;

### Statistical data
Relevant statistical value after the completion of back-tested for display, As end funds、The total rate of return、Sharpe Ratio、Earnings ratio retracement。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/show_result.png)

&nbsp;

### graph analysis
The following four figures respectively represent net account、Net retracement、Daily profit and loss、Profit and loss distribution。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/show_result_chat.png)


&nbsp;
### Kline graph
KLine is based on FIG.PyQtGraphdeveloping，The entire block consists of the following five components：

- BarManager：KLine sequence data management tools
- ChartItem：Basic graphics classes，After inheriting implementation may drawKline、Volume、Technical indicators
- DatetimeAxis：AgainstKCustom designed stamp coordinate axis
- ChartCursor：Cross cursor control，Data for displaying details of a particular location
- ChartWidget：It contains all of the above section，Plotted as a function to provide a single assembly inlet
  
After completion of backtesting，Click on“KLine chart”Button to display historyKLine market data（default1minute），And identifies specific points of sale，As shown below。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/bar_chart.png)


&nbsp;

## Parameter optimization
vnpyprovide2Parameter optimization kinds of solutions：Exhaustive algorithm、Genetic Algorithms


&nbsp;

### Exhaustive algorithm

Exhaustive algorithm principle：
- Enter the name of the parameters to be optimized、Optimization interval、The optimum step，And the optimization target。
```
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
```

&nbsp;


- Global parameter combination is formed, Data structure[{key: value, key: value}, {key: value, key: value}]。
```
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


- Through each combination of the parameters in the global：Ergodic process that is running a strategy backtesting，Optimization of the target value and returns；Then sort the target value，Output optimization results。
```
    def run_optimization(self, optimization_setting: OptimizationSetting, output=True):
        """"""
        # Get optimization setting and target
        settings = optimization_setting.generate_setting()
        target_name = optimization_setting.target_name

        if not settings:
            self.output("Optimization of parameter combinations is empty，Please check")
            return

        if not target_name:
            self.output("Optimization target is not set，Please check")
            return

        # Use multiprocessing pool for running backtesting with different setting
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

        if output:
            for value in result_values:
                msg = f"parameter：{value[0]}, aims：{value[1]}"
                self.output(msg)

        return result_values
```




note：can usemultiprocessingLibrary to create multiple processes to achieve parallel optimization。E.g：If the user's computer is2nuclear，The original optimization time1/2；If the computer is10nuclear，The original optimization time1/10。

&nbsp;


Exhaustive arithmetic operations：

- Click on“Parameter optimization”Push button，Will pop up“Optimization parameters”window，Used to set the optimization goal（Such as to maximize the Sharpe ratio、Maximize revenue ratio retracement）And set the parameters to be optimized and optimization interval，Figure。
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/optimize_setting.png)

- After setting the parameters to be optimized，Click on“Optimization parameters”The bottom of the window“confirm”Button to start the callCPUMulti-process multi-core parallel optimization，At the same time log output related information。
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/optimize_log.png)

- Click on“Optimization Results”Button to see the optimization result，FIG combination of parameters is based on a target value（Sharpe Ratio）They are arranged in descending order from。
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/optimize_result.png)


&nbsp;

### Genetic Algorithms

Genetic algorithm principle：

- Enter the name of the parameters to be optimized、Optimization interval、The optimum step，And the optimization target；

- Global parameter combination is formed，The combined data structure is embedded within the list of tuples，which is\[[(key, value), (key, value)] , [(key, value), (key,value)]]，Parameter combinations the global data structure exhaustive algorithm different。The purpose of this is conducive to cross swap between parameters and mutation。
```
    def generate_setting_ga(self):
        """""" 
        settings_ga = []
        settings = self.generate_setting()     
        for d in settings:            
            param = [tuple(i) for i in d.items()]
            settings_ga.append(param)
        return settings_ga
```

&nbsp;


- Forming individual：transferrandom()Acquisition parameters from the global random function parameter combination。
```
        def generate_parameter():
            """"""
            return random.choice(settings)
```

&nbsp;


- Definition of individual variation rules: Ie mutation，The old individual was completely replaced by a new individual。
```
        def mutate_individual(individual, indpb):
            """"""
            size = len(individual)
            paramlist = generate_parameter()
            for i in range(size):
                if random.random() < indpb:
                    individual[i] = paramlist[i]
            return individual,
```

&nbsp;


- Defined evaluation function：The reference is to the individual，which is[(key, value), (key, value)]In the form of parameter combinations，Thendict()Converted tosettingdictionary，And then run back to test，Output target value optimization，The Sharpe ratio、Earnings ratio retracement。(note，Decorator@lru_cacheRole is to cache the results，To avoid double counting the same input face，Genetic algorithms greatly reduce the running time)
```
@lru_cache(maxsize=1000000)
def _ga_optimize(parameter_values: tuple):
    """"""
    setting = dict(parameter_values)

    result = optimize(
        ga_target_name,
        ga_strategy_class,
        setting,
        ga_vt_symbol,
        ga_interval,
        ga_start,
        ga_rate,
        ga_slippage,
        ga_size,
        ga_pricetick,
        ga_capital,
        ga_end,
        ga_mode
    )
    return (result[1],)


def ga_optimize(parameter_values: list):
    """"""
    return _ga_optimize(tuple(parameter_values))
```

&nbsp;

- Genetic algorithms run：transferdeapLibrary algorithm engine to run on Genetic Algorithms，The specific process is as follows。
1）Define the direction of optimization，Such as to maximize the Sharpe ratio；
2）Then randomly acquired individual parameter combination from the global，And the formation of ethnic groups；
3）For all individuals within communities to assess（That run backtesting），Excluding individual and poor performance；
4）The remaining individuals will cross or mutation，The formation of new communities through the assessment and screening；（So far the population is complete once the iterative process）；
5）After several iterations，Reduce differences within populations，Improve the overall adaptability，The final output suggested results。The result is a set of Pareto solution，It can be1Combination of one or more parameters。

note：As the use of@lru_cache, Iteration speed back to the late increase very much，Because many are avoiding duplicate input again backtesting，Direct access to the memory and returns the results。
```
from deap import creator, base, tools, algorithms
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
        ......
        # Set up genetic algorithem
        toolbox = base.Toolbox() 
        toolbox.register("individual", tools.initIterate, creator.Individual, generate_parameter)                          
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)                                            
        toolbox.register("mate", tools.cxTwoPoint)                                               
        toolbox.register("mutate", mutate_individual, indpb=1)               
        toolbox.register("evaluate", ga_optimize)                                                
        toolbox.register("select", tools.selNSGA2)       

        total_size = len(settings)
        pop_size = population_size                      # number of individuals in each generation
        lambda_ = pop_size                              # number of children to produce at each generation
        mu = int(pop_size * 0.8)                        # number of individuals to select for the next generation

        cxpb = 0.95         # probability that an offspring is produced by crossover    
        mutpb = 1 - cxpb    # probability that an offspring is produced by mutation
        ngen = ngen_size    # number of generation
                
        pop = toolbox.population(pop_size)      
        hof = tools.ParetoFront()               # end result of pareto front

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        np.set_printoptions(suppress=True)
        stats.register("mean", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        algorithms.eaMuPlusLambda(
            pop, 
            toolbox, 
            mu, 
            lambda_, 
            cxpb, 
            mutpb, 
            ngen, 
            stats,
            halloffame=hof
        )

        # Return result list
        results = []

        for parameter_values in hof:
            setting = dict(parameter_values)
            target_value = ga_optimize(parameter_values)[0]
            results.append((setting, target_value, {}))
        
        return results
```







