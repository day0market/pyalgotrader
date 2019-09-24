# Scripts policy
ScriptTraderModule provides an interactive program trading and quantitative analysis functions，Strategies and provide a script function to the whole policy of continuous operation。

Therefore, it can be considered directlyPythonSecurities trading clients operate。ItCTAThe difference is that the policy module：
- Breaking the single Exchange，Single subject of restrictions，
- It can be more convenient to implement hedging strategies such as between index futures and a basket of stocks、Cross-species arbitrage、Stock market stock selection scanning automation functions。

&nbsp;

## Jupytermode

### Load Startup
JupyterModel is based scripting engine（ScriptEngine）Driven。First openJupyter notebookRear，Then loading component、Initialization script engine。among them：
```
from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.ctp import CtpGateway
engine = init_cli_trading([CtpGateway])
```

among them：
- Scripting engine can support multiple interfaces connected，Such asCTP、BITMEX、OESWait；
- init_cli_trading(gateways: Sequence[BaseGateway])You may be a plurality of interface class，Passed to the form of a listinit_cli_trading；
- init_cli_tradingCan be consideredvnpyThe sealed initial start function，The main engine、The script engine and other objects package。

&nbsp;

### Connection interface
Different interfaces require different configuration parameters，SimNowThe configuration is as follows：
```
setting = {
    "username": "xxxx",
    "password": "xxxx",
    "Brokers Code": "9999",
    "Transaction Server":"tcp://180.168.146.187：10101",
    "Quotes server":"tcp://180.168.146.187：10111",
    "product name":"simnow_xxx_test",
    "Authorized coding":"0000000000000000",
    "product information": ""
}
engine.connect_gateway(setting,"CTP")
```

settingThe configuration shown below，Other interface configurations can refer tovnpy/gatewayInterface class directorydefault_settingTo fill in。

![](https://static.vnpy.com/upload/temp/82dd7cfd-6a98-4908-a770-582cfb7e69bc.jpg)


&nbsp;

### Query data
Tell us about where the data is stored is connected to the transaction interface and the successful subscription data：
- Level Interface stop pushing the new data to the main engine；
- Main engines maintains aticksThe latest dictionary for caching different subject mattertickdata（The latest cache only）；
- use_dfThe effect is converted intoDataFrameformat，Facilitate data analysis。

&nbsp;

### Subscribe Quotes
subscribe()Function for subscription market information，If you need to subscribe to a basket of contract prices，You can use the list format。
```
engine.subscribe(vt_symbols = ["rb1909.SHFE","rb1910.SHFE"])
```

&nbsp;

## Scripts policy mode

### Load Startup
- If you use scripts strategy mode，You need to write scripts related policy documents in advance，Such asdemo_arbitrage.py,
- Then openVnTrader,In the menu bar"Features"At open"Scripts policy",In the script out of the top of the open window policy/Path-To-demo_arbitrage.py/demo_arbitrage.py，then
- Click the following figure“start up”。
![](https://static.vnpy.com/upload/temp/bf6b06f8-26e9-466b-b3e0-5b3a6f99e6ba.jpg)

&nbsp;

### Scripts policy
Scripts policy paper prepared by the need to follow a certain format,Using a template provided below，Its role is：
- Subscribe to two varieties of the stock market；
- Print contract information；
- At intervals of3Get the latest quotes seconds。
```
from time import sleep
from vnpy.app.script_trader import ScriptEngine

def run(engine: ScriptEngine):
    """"""
    vt_symbols = ["IF1912.CFFEX", "rb2001.SHFE"]

    # Subscribe Quotes
    engine.subscribe(vt_symbols)

    # Get contract information
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        msg = f"Contract Information，{contract}"
        engine.write_log(msg)

    # Continuous operation，usestrategy_activeTo determine whether to exit the program
    while engine.strategy_active:
        # Polling Get Quotes
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f"The latest market, {tick}"
            engine.write_log(msg)

        # wait3Seconds into the next round
        sleep(3)
```

&nbsp;

### Operational control
engine.strategy_activeFor controlWhilecycle，Switch strategy is regarded script：
- Click on“start up”Push button，start upWhilecycle，Script execution policy；
- Click on“stop”Push button，drop outWhilecycle，Stop Scripts policy。

&nbsp;

## Function Function

### A single query

get_tick：A current single querytick，use_dfAn optional parameter，It returns the class object for the conversion intoDataFrameformat，Facilitate data analysis。
```
tick = engine.get_tick(vt_symbol="rb1910.SHFE",use_df=False)
```

among them：
- vt_symbol：Code for the local contract，Format is a contract species+Exchange，Such asrb1910.SHFE。
- use_df：forboolvariable，defaultFalse，returnTickDataClass object，Otherwise, it returns the correspondingDataFrame，Figure。

![](https://static.vnpy.com/upload/temp/d00ca165-1266-4812-afaa-f6723745d6a4.png)

&nbsp;

get_order：according tovt_orderidView details of the orders。
```
order = engine.get_order(vt_orderid='CTP.3_-9351590_1',use_df=False)
```

among them，vt_orderidLocal commission number，When orders under，It will automatically return to the delegatevt_orderid：
- With"CTP.3_-9351590_1"A Case Study，It consists ofctpInterfacename,frontid,sessionid,order_refStructure；
- frontidwithsessionidinvnpyconnectCTPAfter interface consists ofCTPCallback produce；
- order_refYesvnpyInternal maintenance for distinguishingorderA variable。

![](https://static.vnpy.com/upload/temp/ae9f6d7f-49da-41e4-a862-825bf146118d.png)

&nbsp;

get_contract：According to localvt_symbolDetailed information corresponding to query object contract。
```
contract = engine.get_contract(vt_symbol="rb1910.SHFE",use_df=False)
```

![](https://static.vnpy.com/upload/temp/4111776b-91fd-44e6-8b2c-289961862a3a.jpg)

&nbsp;

get_bars：Query historical data。（Need to initializeRQDataClient）
```
bars = engine.get_bars(vt_symbol="rb1910.SHFE",start_date="20190101",
                        interval=Interval.MINUTE,use_df=False)
```

among them：
- vt_symbol：Local Contracts Code。
- start_date：Start Date，The format must be"%Y%m%d"。
- interval：KLine cycle，include：minute、hour、day、week
- bars：It contains a series ofBarDataA list of object data，itsBarDataIt is defined as follows：
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

get_position：according tovt_positionidTo query the position situation，Return the object containing the name of the interface、Exchange、Contracts Code、Quantity、Freeze quantity, etc.。
```
position = engine.get_position(vt_positionid='rb1909.SHFE.Direction.LONG')
```
note，vt_positionidforvnpyFor a sum of specific positions inside a unique position number，The format"vt_symbol.Direction.LONG",Optional multi-direction positions wherein the cartridge、Short positions and net position，Figure。

![](https://static.vnpy.com/upload/temp/4c585dac-0ac9-4fd8-9926-ddc104512359.jpg)

&nbsp;

### Multiple queries
get_ticks：Query multiple new contractstick。
```
ticks = engine.get_ticks(vt_symbols=['rb1910.SHFE','rb1909.SHFE'],use_df = True)
```

vt_symbolsIt is a list format，Which contains morevt_symbol，Figure。

![](https://static.vnpy.com/upload/temp/311e1ee8-1a3d-496f-833f-bbb7a3a624ab.png)

&nbsp;

get_orders：According to query multiplevt_orderidQuery its details。vt_orderidsThe list，Which contains morevt_orderid
```
orders = engine.get_orders([orderid_one,orderid_two],use_df=True)
```


&nbsp;

get_trades：According to a givenvt_orderidReturn all the declaration processTradeDataObjects。vt_orderidIs a local commission number，Each delegateOrderData，As part of the transaction relationship，It may correspond to a multi-pen dealTradeData。
```
trades = engine.get_trades(vt_orderid = your_vt_orderid,use_df = True)
```

&nbsp;

### The full amount of inquiries

In the full amount of the query，The only parameter isuse_df，The default isFalse，It returns a corresponding data containingListObjects,E.gContractData，AccountData，PositionData。

- get_all_contracts：It returns a defaultlist，It includes a full marketContractData，in caseuse_df=TrueThe corresponding returnDataFrame；
- get_all_active_orders：Activity refers to the commission entrusted entirely to wait for the transaction，So the state comprising“Submitted、No transactions、Part of the transaction”；The function returns a series ofOrderDataThe list of objects；
- get_all_accounts：Returns a defaultAccountDataThe list of objects；
- get_all_position：Returns a defaultPositionDataThe list of objects，Figure。

![](https://static.vnpy.com/upload/temp/5d698a27-545b-46bb-9d16-428a8ccb7956.png)

&nbsp;

### Trading commission

For example in order to entrust to buy，engine.buy()The function parameters comprises：
- vt_symbol：Local Contracts Code（String format）
- price：Price declaration（Floating-point type）;
- volume：Number of declaration（Floating-point type）;
- order_type：OrderTypeEnumeration constant，The default is a limit order（OrderType.LIMIT），Supports single stop（OrderType.STOP）、FAK（OrderType.FAK）、FOK（OrderType.FOK）、Market Order（OrderType.MARKET），Exchange supports different ways declaration is not exactly the same。
```
engine.buy(vt_symbol = "rb1910.SHFE",price = "3200",volume = "1",order_type=OrderType.LIMIT)
```

No commission will return after performing local trading commissionvt_orderid，Withdrawals, also based on the number of local delegate
```
engine.cancel_order(vt_orderid = 'CTP.3_-9351590_1')
```

&nbsp;

### Information output
write_log()Transactions function can be used to record the time of sale，The information output under the column blank script window policy。

&nbsp;

send_email()Function for real-time throughemailInform the user policy operation：
- In the firstvt_setting.jsonConfigurationemailRelated Information；
- Mail title“Scripts policy engine notification”；
- msgString format，It represents the message body content，Figure。
```
engine.send_email(msg = "Your Msg")
```

![](https://static.vnpy.com/upload/temp/8dd8d6b0-6c04-4cb4-a426-ad43d11a13eb.png)

Before using mailboxes need to openSMTPservice。
- email.server：Mail server address，vnpyThe default fill upQQE-mail server address，Can be directly used without change，If you need to use another mailbox，Needs of their own to find what other server address。
- email.port：Mail server port number，vnpmDefault filled outQQMail server port，Can be directly used。
- email.username：Fill in the e-mail address to，Such asxxxx@qq.com。
- email.password：forQQmailbox，Here is not the mail password，But openingSMTPAfter an authorization code generated by the system。
- email.sendert：email.username。
- email.receiver：Accept mail e-mail address，such asxxxx@outlook.com。
