# CTA backtesting module 
CTA backtesting module is based on PyQt5 with pyqtgraph graphical back-tested tool .  start up VN Trader rear ， in the menu bar “ features -> CTA backtesting ” to enter the graphical interface backtesting ， as shown below . CTA backtesting module mainly realizes 3 function ： download historical market data ,  strategy backtesting ,  parameter optimization , K line chart point of sale display . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/cta_backtester.png)

&nbsp;

##  load startup 
 backtesting into the graphical interface “CTA backtesting ” rear ， initial work will be completed soon ： backtesting engine initialization ,  initialization RQData client . 

```
    def init_engine(self):
        """"""
        self.write_log(" initialization CTA backtesting engine ")

        self.backtesting_engine = BacktestingEngine()
        # Redirect log from backtesting engine outside.
        self.backtesting_engine.output = self.write_log

        self.write_log(" policy file loaded ")

        self.init_rqdata()

    def init_rqdata(self):
        """
        Init RQData client.
        """
        result = rqdata_client.init()
        if result:
            self.write_log("RQData successful initialization data interface ")
```

&nbsp;


##  download data 
 before starting strategy backtesting ， we must ensure that there is sufficient historical data in the database .  therefore vnpy it provides a historical data download function keys . 

### RQData
RQData provide domestic stock , ETF,  historical data of futures and options . 
 its main function is to download data based on RQData of get_price() function to achieve . 
```
get_price(
    order_book_ids, start_date='2013-01-04', end_date='2014-01-04',
    frequency='1d', fields=None, adjust_type='pre', skip_suspended =False,
    market='cn'
)
```


 before use to ensure that RQData initialized ， then fill in the following 4 field information ：
-  native code ： variety contract format + exchange ， such as IF88.CFFEX, rb88.SHFE； then at the bottom by RqdataClient of to_rq_symbol() function into line with RQData format ， correspond RQData in get_price() function order_book_ids field . 
- K line cycle ： you can fill 1m, 1h, d, w， correspond get_price() function frequency field . 
-  start date ： the format yy/mm/dd， such as 2017/4/21， correspond get_price() function start_date field . （ click the window on the right arrow button to change the date size ）
-  end date ： the format yy/mm/dd， such as 2019/4/22， correspond get_price() function end_date field . （ click the window on the right arrow button to change the date size ）
  
 after filling out the information fields ， click below “ download data ” button to start the download ， download the success shown in fig. . 


![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/data_loader.png)

&nbsp;

### IB

 interactive brokers offers external disk stock ,  futures ,  historical data option . 
 before downloading must be connected IB interface ， because of its function is mainly based on download data IbGateway class query_history() function to achieve . 

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

BITMEX currency exchange provides digital historical data . 
 due to differences in the simulation environment and market environment is big firm ， therefore you need to log in with a firm account BIMEX interface to download real market data ， its main function is to download data based on BitmexGateway class query_history() function to achieve . 

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
                msg = f" failure to obtain historical data ， status code ：{resp.status_code}， information ：{resp.text}"
                self.gateway.write_log(msg)
                break
            else:
                data = resp.json()
                if not data:
                    msg = f" obtain historical data is empty ， starting time ：{start_time}， quantity ：{count}"
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
                msg = f" get historical success ，{req.symbol} - {req.interval.value}，{begin} - {end}"
                self.gateway.write_log(msg)

                # Break if total data count less than 750 (latest date collected)
                if len(data) < 750:
                    break

                # Update start time
                start_time = bar.datetime + TIMEDELTA_MAP[req.interval]

        return history
```

&nbsp;

##  strategy backtesting 
 after downloading historical data ， configure the following fields ： trading straregy ,  fee rate ,  trading slippage ,  contract multiplier ,  price beat ,  backtesting funds . 
 these fields correspond to major BacktesterEngine category run_backtesting function . 

 if the historical data already exists in the database ， without re-downloading ， import data directly from the local database back the measured .  note ，vt_symbol the item code format . in the form of exchange of ， such as IF1908.CFFEX， import will automatically be divided into two types and exchanges 

```
def run_backtesting(
    self, class_name: str, vt_symbol: str, interval: str, start: datetime, 
    end: datetime, rate: float, slippage: float, size: int, pricetick: float, 
    capital: int, setting: dict
)：
```


 click below “ start backtesting ” button to start backtesting ：
 first, the parameters window will pop up as shown in fig. ， for adjusting the policy parameters .  this setting corresponds to the run_backtesting() function setting dictionary . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/parameter_setting.png)



 click on “ confirm ” button starts running back to test ， at the same time the log information interface will output ， figure . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/backtesting_log.png)

 statistics chart will show back-tested after completion . 

&nbsp;

###  statistical data 
 relevant statistical value after the completion of back-tested for display ,  as end funds ,  the total rate of return ,  sharpe ratio ,  earnings ratio retracement . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/show_result.png)

&nbsp;

###  graph analysis 
 the following four figures respectively represent net account ,  net retracement ,  daily profit and loss ,  profit and loss distribution . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/show_result_chat.png)


&nbsp;
### K line graph 
K line is based on fig. PyQtGraph developing ， the entire block consists of the following five components ：

- BarManager：K line sequence data management tools 
- ChartItem： basic graphics classes ， after inheriting implementation may draw K line ,  volume ,  technical indicators 
- DatetimeAxis： against K custom designed stamp coordinate axis 
- ChartCursor： cross cursor control ， data for displaying details of a particular location 
- ChartWidget： contains all of the above section ， plotted as a function to provide a single assembly inlet 
  
 after completion of backtesting ， click on “K line chart ” button to display history K line market data （ default 1 minute ）， and identifies specific points of sale ， as shown below . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/bar_chart.png)


&nbsp;

##  parameter optimization 
vnpy provide 2 parameter optimization kinds of solutions ： exhaustive algorithm ,  genetic algorithms 


&nbsp;

###  exhaustive algorithm 

 exhaustive algorithm principle ：
-  enter the name of the parameters to be optimized ,  optimization interval ,  the optimum step ， and the optimization target . 
```
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
```

&nbsp;


-  global parameter combination is formed ,  data structure [{key: value, key: value}, {key: value, key: value}]. 
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


-  through each combination of the parameters in the global ： ergodic process that is running a strategy backtesting ， optimization of the target value and returns ； then sort the target value ， output optimization results . 
```
    def run_optimization(self, optimization_setting: OptimizationSetting, output=True):
        """"""
        # Get optimization setting and target
        settings = optimization_setting.generate_setting()
        target_name = optimization_setting.target_name

        if not settings:
            self.output(" optimization of parameter combinations is empty ， please check ")
            return

        if not target_name:
            self.output(" optimization target is not set ， please check ")
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
                msg = f" parameter ：{value[0]},  aims ：{value[1]}"
                self.output(msg)

        return result_values
```




 note ： can use multiprocessing library to create multiple processes to achieve parallel optimization .  e.g ： if the user's computer is 2 nuclear ， the original optimization time 1/2； if the computer is 10 nuclear ， the original optimization time 1/10. 

&nbsp;


 exhaustive arithmetic operations ：

-  click on “ parameter optimization ” push button ， will pop up “ optimization parameters ” window ， used to set the optimization goal （ such as to maximize the sharpe ratio ,  maximize revenue ratio retracement ） and set the parameters to be optimized and optimization interval ， figure . 
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/optimize_setting.png)

-  after setting the parameters to be optimized ， click on “ optimization parameters ” the bottom of the window “ confirm ” button to start the call CPU multi-process multi-core parallel optimization ， at the same time log output related information . 
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/optimize_log.png)

-  click on “ optimization results ” button to see the optimization result ， fig combination of parameters is based on a target value （ sharpe ratio ） they are arranged in descending order from . 
  
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/cta_backtester/optimize_result.png)


&nbsp;

###  genetic algorithms 

 genetic algorithm principle ：

-  enter the name of the parameters to be optimized ,  optimization interval ,  the optimum step ， and the optimization target ；

-  global parameter combination is formed ， the combined data structure is embedded within the list of tuples ， which is \[[(key, value), (key, value)] , [(key, value), (key,value)]]， parameter combinations the global data structure exhaustive algorithm different .  the purpose of this is conducive to cross swap between parameters and mutation . 
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


-  forming individual ： transfer random() acquisition parameters from the global random function parameter combination . 
```
        def generate_parameter():
            """"""
            return random.choice(settings)
```

&nbsp;


-  definition of individual variation rules :  ie mutation ， the old individual was completely replaced by a new individual . 
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


-  defined evaluation function ： the reference is to the individual ， which is [(key, value), (key, value)] in the form of parameter combinations ， then dict() converted to setting dictionary ， and then run back to test ， output target value optimization ， the sharpe ratio ,  earnings ratio retracement . ( note ， decorator @lru_cache role is to cache the results ， to avoid double counting the same input face ， genetic algorithms greatly reduce the running time )
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

-  genetic algorithms run ： transfer deap library algorithm engine to run on genetic algorithms ， the specific process is as follows . 
1） define the direction of optimization ， such as to maximize the sharpe ratio ；
2） then randomly acquired individual parameter combination from the global ， and the formation of ethnic groups ；
3） for all individuals within communities to assess （ that run backtesting ）， excluding individual and poor performance ；
4） the remaining individuals will cross or mutation ， the formation of new communities through the assessment and screening ；（ so far is a complete population iterative process ）；
5） after several iterations ， reduce differences within populations ， improve the overall adaptability ， the final output suggested results .  the result is a set of pareto solution ， it can be 1 combination of one or more parameters . 

 note ： as the use of @lru_cache,  iteration speed back to the late increase very much ， because many are avoiding duplicate input again backtesting ， direct access to the memory and returns the results . 
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







