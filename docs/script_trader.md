#  scripts policy 
ScriptTrader module provides an interactive program trading and quantitative analysis functions ， strategies and provide a script function to the whole policy of continuous operation . 

 therefore, it can be considered directly Python securities trading clients operate .  it CTA the difference is that the policy module ：
-  breaking the single exchange ， single subject of restrictions ，
-  it can be more convenient to implement hedging strategies such as between index futures and a basket of stocks ,  cross-species arbitrage ,  stock market stock selection scanning automation functions . 

&nbsp;

## Jupyter mode 

###  load startup 
Jupyter model is based scripting engine （ScriptEngine） driven .  first open Jupyter notebook rear ， then loading component ,  initialization script engine .  among them ：
```
from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.ctp import CtpGateway
engine = init_cli_trading([CtpGateway])
```

 among them ：
-  scripting engine can support multiple interfaces connected ， such as CTP, BITMEX, OES wait ；
- init_cli_trading(gateways: Sequence[BaseGateway]) you may be a plurality of interface class ， passed to the form of a list init_cli_trading；
- init_cli_trading can be considered vnpy the sealed initial start function ， the main engine ,  the script engine and other objects package . 

&nbsp;

###  connection interface 
 different interfaces require different configuration parameters ，SimNow the configuration is as follows ：
```
setting = {
    " username ": "xxxx",
    " password ": "xxxx",
    " brokers code ": "9999",
    " transaction server ":"tcp://180.168.146.187：10101",
    " quotes server ":"tcp://180.168.146.187：10111",
    " product name ":"simnow_xxx_test",
    " authorized coding ":"0000000000000000",
    " product information ": ""
}
engine.connect_gateway(setting,"CTP")
```

setting the configuration shown below ， other interface configurations can refer to vnpy/gateway interface class directory default_setting to fill in . 

![](https://static.vnpy.com/upload/temp/82dd7cfd-6a98-4908-a770-582cfb7e69bc.jpg)


&nbsp;

###  query data 
 tell us about where the data is stored is connected to the transaction interface and the successful subscription data ：
-  level interface stop pushing the new data to the main engine ；
-  main engines maintains a ticks the latest dictionary for caching different subject matter tick data （ the latest cache only ）；
- use_df the effect is converted into DataFrame format ， facilitate data analysis . 

&nbsp;

###  subscribe quotes 
subscribe() function for subscription market information ， if you need to subscribe to a basket of contract prices ， you can use the list format . 
```
engine.subscribe(vt_symbols = ["rb1909.SHFE","rb1910.SHFE"])
```

&nbsp;

##  scripts policy mode 

###  load startup 
-  if you use scripts strategy mode ， you need to write scripts related policy documents in advance ， such as demo_arbitrage.py,
-  then open VnTrader, in the menu bar " features " at open " scripts policy ", in the script out of the top of the open window policy /Path-To-demo_arbitrage.py/demo_arbitrage.py， then 
-  click the following figure “ start up ”. 
![](https://static.vnpy.com/upload/temp/bf6b06f8-26e9-466b-b3e0-5b3a6f99e6ba.jpg)

&nbsp;

###  scripts policy 
 scripts policy paper prepared by the need to follow a certain format , using a template provided below ， its role is ：
-  subscribe to two varieties of the stock market ；
-  print contract information ；
-  at intervals of 3 get the latest quotes seconds . 
```
from time import sleep
from vnpy.app.script_trader import ScriptEngine

def run(engine: ScriptEngine):
    """"""
    vt_symbols = ["IF1912.CFFEX", "rb2001.SHFE"]

    #  subscribe quotes 
    engine.subscribe(vt_symbols)

    #  get contract information 
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        msg = f" contract information ，{contract}"
        engine.write_log(msg)

    #  continuous operation ， use strategy_active to determine whether to exit the program 
    while engine.strategy_active:
        #  polling get quotes 
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f" the latest market , {tick}"
            engine.write_log(msg)

        #  wait 3 seconds into the next round 
        sleep(3)
```

&nbsp;

###  operational control 
engine.strategy_active for control While cycle ， switch strategy is regarded script ：
-  click on “ start up ” push button ， start up While cycle ， script execution policy ；
-  click on “ stop ” push button ， drop out While cycle ， stop scripts policy . 

&nbsp;

##  function function 

###  a single query 

get_tick： a current single query tick，use_df an optional parameter ， it returns the class object for the conversion into DataFrame format ， facilitate data analysis . 
```
tick = engine.get_tick(vt_symbol="rb1910.SHFE",use_df=False)
```

 among them ：
- vt_symbol： code for the local contract ， format is a contract species + exchange ， such as rb1910.SHFE. 
- use_df： for bool variable ， default False， return TickData class object ， otherwise, it returns the corresponding DataFrame， figure . 

![](https://static.vnpy.com/upload/temp/d00ca165-1266-4812-afaa-f6723745d6a4.png)

&nbsp;

get_order： according to vt_orderid view details of the orders . 
```
order = engine.get_order(vt_orderid='CTP.3_-9351590_1',use_df=False)
```

 among them ，vt_orderid local commission number ， when orders under ， it will automatically return to the delegate vt_orderid：
-  with "CTP.3_-9351590_1" a case study ， it consists of ctp interface name,frontid,sessionid,order_ref structure ；
- frontid with sessionid in vnpy connect CTP after interface consists of CTP callback produce ；
- order_ref yes vnpy internal maintenance for distinguishing order a variable . 

![](https://static.vnpy.com/upload/temp/ae9f6d7f-49da-41e4-a862-825bf146118d.png)

&nbsp;

get_contract： according to local vt_symbol detailed information corresponding to query object contract . 
```
contract = engine.get_contract(vt_symbol="rb1910.SHFE",use_df=False)
```

![](https://static.vnpy.com/upload/temp/4111776b-91fd-44e6-8b2c-289961862a3a.jpg)

&nbsp;

get_bars： query historical data . （ need to initialize RQData client ）
```
bars = engine.get_bars(vt_symbol="rb1910.SHFE",start_date="20190101",
                        interval=Interval.MINUTE,use_df=False)
```

 among them ：
- vt_symbol： local contracts code . 
- start_date： start date ， the format must be "%Y%m%d". 
- interval：K line cycle ， include ： minute ,  hour ,  day ,  week 
- bars： it contains a series of BarData a list of object data ， its BarData it is defined as follows ：
```
@dataclass
class BarData(BaseData):

    symbol: str
    exchange: Exchange
    datetime: datetime
    interval: Interval = None
    volume: float = 0
    open_interest: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

    def __post_init__(self):
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
```

&nbsp;

get_position： according to vt_positionid to query the position situation ， return the object containing the name of the interface ,  exchange ,  contracts code ,  quantity ,  freeze quantity, etc. . 
```
position = engine.get_position(vt_positionid='rb1909.SHFE.Direction.LONG')
```
 note ，vt_positionid for vnpy for a sum of specific positions inside a unique position number ， the format "vt_symbol.Direction.LONG", optional multi-direction positions wherein the cartridge ,  short positions and net position ， figure . 

![](https://static.vnpy.com/upload/temp/4c585dac-0ac9-4fd8-9926-ddc104512359.jpg)

&nbsp;

###  multiple queries 
get_ticks： query multiple new contracts tick. 
```
ticks = engine.get_ticks(vt_symbols=['rb1910.SHFE','rb1909.SHFE'],use_df = True)
```

vt_symbols it is a list format ， which contains more vt_symbol， figure . 

![](https://static.vnpy.com/upload/temp/311e1ee8-1a3d-496f-833f-bbb7a3a624ab.png)

&nbsp;

get_orders： according to query multiple vt_orderid query its details . vt_orderids the list ， which contains more vt_orderid
```
orders = engine.get_orders([orderid_one,orderid_two],use_df=True)
```


&nbsp;

get_trades： according to a given vt_orderid return all the declaration process TradeData objects . vt_orderid is a local commission number ， each delegate OrderData， as part of the transaction relationship ， it may correspond to a multi-pen deal TradeData. 
```
trades = engine.get_trades(vt_orderid = your_vt_orderid,use_df = True)
```

&nbsp;

###  the full amount of inquiries 

 in the full amount of the query ， the only parameter is use_df， the default is False， it returns a corresponding data containing List objects , e.g ContractData，AccountData，PositionData. 

- get_all_contracts： it returns a default list， it includes a full market ContractData， in case use_df=True the corresponding return DataFrame；
- get_all_active_orders： activity refers to the commission entrusted entirely to wait for the transaction ， so the state comprising “ submitted ,  no transactions ,  part of the transaction ”； the function returns a series of OrderData the list of objects ；
- get_all_accounts： returns a default AccountData the list of objects ；
- get_all_position： returns a default PositionData the list of objects ， figure . 

![](https://static.vnpy.com/upload/temp/5d698a27-545b-46bb-9d16-428a8ccb7956.png)

&nbsp;

###  trading commission 

 for example in order to entrust to buy ，engine.buy() the function parameters comprises ：
- vt_symbol： local contracts code （ string format ）
- price： price declaration （ floating-point type ）;
- volume： number of declaration （ floating-point type ）;
- order_type：OrderType enumeration constant ， the default is a limit order （OrderType.LIMIT）， supports single stop （OrderType.STOP）, FAK（OrderType.FAK）, FOK（OrderType.FOK）,  market order （OrderType.MARKET）， exchange supports different ways declaration is not exactly the same . 
```
engine.buy(vt_symbol = "rb1910.SHFE",price = "3200",volume = "1",order_type=OrderType.LIMIT)
```

 no commission will return after performing local trading commission vt_orderid， withdrawals, also based on the number of local delegate 
```
engine.cancel_order(vt_orderid = 'CTP.3_-9351590_1')
```

&nbsp;

###  information output 
write_log() transactions function can be used to record the time of sale ， the information output under the column blank script window policy . 

&nbsp;

send_email() function for real-time through email inform the user policy operation ：
-  in the first vt_setting.json configuration email related information ；
-  mail title “ scripts policy engine notification ”；
- msg string format ， it represents the message body content ， figure . 
```
engine.send_email(msg = "Your Msg")
```

![](https://static.vnpy.com/upload/temp/8dd8d6b0-6c04-4cb4-a426-ad43d11a13eb.png)

 before using mailboxes need to open SMTP service . 
- email.server： mail server address ，vnpy the default fill up QQ e-mail server address ， can be directly used without change ， if you need to use another mailbox ， needs of their own to find what other server address . 
- email.port： mail server port number ，vnpm default filled out QQ mail server port ， can be directly used . 
- email.username： fill in the e-mail address to ， such as xxxx@qq.com. 
- email.password： for QQ mailbox ， here is not the mail password ， but opening SMTP after an authorization code generated by the system . 
- email.sendert：email.username. 
- email.receiver： accept mail e-mail address ， such as xxxx@outlook.com. 
