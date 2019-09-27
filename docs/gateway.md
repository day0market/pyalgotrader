#  trading interface 

##  how to connect 

 from gateway folder on the introduction of the interface program ， by add_gateway() function mobilize ， the final show to the graphical user interface VN Trader in . 

 in the menu bar " system "->" connection CTP” button will pop up as account configuration window ， enter the account number ,  passwords and other information that is relevant connection interface ， and immediately carry out inquiries :  such as query account information ,  queries positions ,  information inquiry commission ,  query transaction information . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/gateway/login.png)

&nbsp;

###  load interface needs with 

 example charging interface in the root directory "tests\trader" folder run.py file . 
-  from gateway the introduction of file folders interface class ， such as from vnpy.gateway.ctp import CtpGateway;
-  and by creating an event engine object add_gateway() add function interface program ;
-  creating graphical objects main_window， with VN Trader interface show up . 


```
from vnpy.gateway.ctp import CtpGateway

def main():
    """"""
    qapp = create_qapp()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()
```

&nbsp;


###  configuration and connection 

 turn on cmd window ， use the command “Python run.py" to enter VN Trader user interface .  click on the top left of the menu bar " system "->" connection CTP” button configuration window will pop account ， enter the account number ,  passwords and other information that is relevant connection interface . 

 process connection interface is first initialized account information ， then call connet() function to connect the port and market trading port . 
-  trading port ： query user information （ as account funds ,  positions ,  commissioned record ,  transaction record ）,  queries can be traded contract information ,  hanging cancellation operation ；
-  quotes port ： subscribe to receive stock market information push ,  receiving a user-related information （ such as account money to upgrade ,  position update ,  push commission ,  push deal ） update callback push . 


&nbsp;


###  modify json profiles 

 related stored in interface configuration json file ， in figure C under disk user directory .vntrader folder . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/gateway/.vntrader.png)

 so you want to modify the interface configuration file ， i.e., the user interface may be a graphical VN Trader in the modification ， can also directly in .vntrader modify json file . 
 in addition to json profile separate from vnpy benefit is ： avoid each upgrade must be reconfigured json file . 


&nbsp;


###  view tradable contracts 

 interface login first ， then click on the menu bar " help "->" query contract ” button blank “ query contract ” window .  click on “ inquire ” button will display the query results ， figure . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/gateway/query_contract.png)



&nbsp;

##  interface category 

|  interface      |                     types of                     |
| -------- | :----------------------------------------: |
| CTP      |                     futures                     |
| MINI     |                     futures                     |
| FEMAS    |                     futures                     |
| XTP      |  domestic stock ,  index ,  fund ,  bond ,  options ,  margin  |
| OES      |                   domestic stock                   |
| TORA     |                   domestic stock                   |
| IB       |             external disk stock ,  futures ,  options             |
| TAP      |                external disk futures ,  options                |
| FUTU     |             domestic stock ,  hong kong stocks ,  us stocks             |
| TIGER    |             domestic stock ,  hong kong stocks ,  us stocks             |
| ALPACA   |                     us stocks                     |
| BITFINEX |                   digital currency                   |
| BITMEX   |                   digital currency                   |
| BINANCE  |                   digital currency                   |
| OKEX     |                   digital currency                   |
| OKEXF    |                   digital currency                   |
| HUOBI    |                   digital currency                   |
| HBDM     |                   digital currency                   |
| ONETOKEN |                   digital currency                   |
| RPC      |                  RPC service                    |



&nbsp;


##  detailed interface 

### CTP

####  how to load 

run.py document provides the interface load sample ： start with gateway on call ctpGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.ctp import CtpGateway
main_engine.add_gateway(CtpGateway)
```

&nbsp;

####  related fields 

-  username ：username
-  password ：password：
-  broker no. ：brokerid
-  transaction server address ：td_address
-  quotes server address ：md_address
-  product name ：product_info
-  authorized coding ：auth_code
  
&nbsp;

####  account acquisition 

-  simulation account ： from SimNow get on the site .  simply enter the phone number and the sms verification can be . （ sms verification sometimes can only receive normal working hours on weekdays ）SimNow the user name 6 pure digital bits ， broker no. 9999， and provide 2 environmental simulation test suite for intraday trading and after-hours . 
  
-  firm account ： in the futures company account ， can be opened by contacting customer manager .  a user named pure digital ， brokers also a number 4 pure digital bits . （ each futures broker's numbers are different ） other ， a firm offer trading accounts can be opened emulation function ， also you need to contact customer manager . 


&nbsp;

### MINI

####  how to load 

 start with gateway on call MiniGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.mini import MiniGateway
main_engine.add_gateway(MiniGateway)
```

&nbsp;

####  related fields 

-  username ：username
-  password ：password：
-  broker no. ：brokerid
-  transaction server address ：td_address
-  quotes server address ：md_address
-  product name ：product_info
-  authorized coding ：auth_code
  
&nbsp;

####  account acquisition 

 in the futures company account ， can be opened by contacting customer manager .  a user named pure digital ， brokers also a number 4 pure digital bits . （ each futures broker's numbers are different ） other ， a firm offer trading accounts can be opened emulation function ， also you need to contact customer manager . 


&nbsp;

###  pegasus （FEMAS）

####  how to load 

 start with gateway on call FemasGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.femas import FemasGateway
main_engine.add_gateway(FemasGateway)
```

&nbsp;

####  related fields 

-  username ：username
-  password ：password：
-  broker no. ：brokerid
-  transaction server address ：td_address
-  quotes server address ：md_address
-  product name ：product_info
-  authorized coding ：auth_code
  
&nbsp;

####  account acquisition 

 in the futures company account ， can be opened by contacting customer manager .  a user named pure digital ， brokers also a number 4 pure digital bits . （ each futures broker's numbers are different ） other ， a firm offer trading accounts can be opened emulation function ， also you need to contact customer manager . 


&nbsp;



###  counter in thailand (XTP)

####  how to load 

 start with gateway on call XtpGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.xtp import XtpGateway
main_engine.add_gateway(XtpGateway)
```

&nbsp;


####  related fields 

-  account number ：
-  password ：
-  client number ": 1
-  quotes address ：
-  quotes port ": 0
-  trading address ：
-  trading port ": 0
-  quotes agreement : ["TCP", "UDP"]
-  authorization code ：

&nbsp;


####  account acquisition 

 test account please contact the thai securities and application . 

####  other features 

XTP it is the first to provide the margin of speed counter . 

&nbsp;


###  wide rui counter (OES)

####  how to load 

 start with gateway on call OesGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.oes import OesGateway
main_engine.add_gateway(OesGateway)
```

&nbsp;


####  related fields 

-  username ：username
-  password ：password
-  hard disk serial number ：hdd_serial
-  trading commission server ：td_ord_server
-  transaction server returns ：td_rpt_server
-  trading query server ：td_qry_server
-  quotes push server ：md_tcp_server
-  quotes query server ：md_qry_server

&nbsp;


####  account acquisition 

 wide test account please contact core technology application 

&nbsp;

####  other features 

 rui counter offer wide network UDP low-latency multicast quotes and real-time transaction information push . 

&nbsp;


###  华鑫奇 point (TORA)

####  how to load 

 start with gateway on call ToraGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.tota import ToraGateway
main_engine.add_gateway(OesGateway)
```

&nbsp;

####  related fields 

-  account number : username
-  password : password
-  transaction server : td_address
-  quotes server : md_address

&nbsp;

####  account acquisition 

 test account please contact huaxin securities application 


&nbsp;

###  interactive brokers (IB)

####  how to load 

 start with gateway on call IbGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.ib import IbGateway
main_engine.add_gateway(IbGateway)
```

&nbsp;


####  related fields 

- TWS address ：127.0.0.1
- TWS port ：7497
-  client number ：1


&nbsp;


####  account acquisition 

 available at interactive brokers account and deposit after API access rights .  it has a firm offer to open an account before they can apply for mock trading account . 

&nbsp;

####  other features 

 tradable varieties almost global coverage of stock ,  options ,  options ； relatively low fees . 

 note IB contract interface code more special ， go to the official website of the sector inquiry product inquiry ，VN Trader use interactive brokers is a unique identifier for each contract at a certain exchange ConId as contract code ， rather than Symbol or LocalName. 

&nbsp;


###  yi sheng external disk (TAP)

####  how to load 

 start with gateway on call TapGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.tap import TapGateway
main_engine.add_gateway(TapGateway)
```

&nbsp;


####  related fields 

-  authorization code ：auth code
-  quotes account ：quote username
-  quotes password ：quote password
-  quotes address ：123.15.58.21
-  quotes port ：7171



&nbsp;


####  account acquisition 

 in TAP after the deposit to open an account and get API access rights . 

&nbsp;


###  fu passers securities (FUTU)

####  how to load 

 start with gateway on call FutuGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.futu import FutuGateway
main_engine.add_gateway(FutuGateway)
```

&nbsp;


####  related fields 

-  address ：127.0.0.1
-  password ：
-  port ：11111
-  market ：HK  or  US
-  surroundings ：TrdEnv.REAL  or  TrdEnv.SIMULATE


&nbsp;


####  account acquisition 

 rich in transit securities account and can get back into gold API access rights .  it has a firm offer to open an account before they can apply for mock trading account . 






&nbsp;

###  tiger securities (TIGER)


####  how to load 

 start with gateway on call TigerGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.tiger import TigerGateway
main_engine.add_gateway(TigerGateway)
```

&nbsp;


####  related fields 

-  user ID：tiger_id
-  global account ：account
-  standard account ：standard_account
-  hi钥 ：private_key



&nbsp;


####  account acquisition 

 tiger securities account and can get back into gold API access rights .  it has a firm offer to open an account before they can apply for mock trading account . 


&nbsp;


### ALPACA

####  how to load 
 start with gateway on call AlpacaGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.alpaca import AlpacaGateway
main_engine.add_gateway(AlpacaGateway)
```

&nbsp;

####  related fields 
- KEY ID: key
- Secret Key: secret
-  sessions : 10
-  server :["REAL", "PAPER"]
####  account acquisition 
 in OKEX official cape households and can get back into gold API access rights . 
####  other features 

&nbsp;


### BITMEX

####  how to load 

 start with gateway on call BitmexGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.bitmex import BitmexGateway
main_engine.add_gateway(BitmexGateway)
```

&nbsp;


####  related fields 

-  user ID：ID
-  password ：Secret
-  sessions ：3
-  server ：REAL  or  TESTNET
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 in BITMEX official cape households and can get back into gold API access rights . 



&nbsp;

### OKEX stock （OKEX）


####  how to load 

 start with gateway on call OkexGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.okex import OkexGateway
main_engine.add_gateway(OkexGateway)
```

&nbsp;


####  related fields 

- API hi钥 ：API Key
-  cryptographic key ：Secret Key
-  sessions ：3
-  password ：passphrase
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 in OKEX official cape households and can get back into gold API access rights . 



&nbsp;


### OKEX futures （OKEXF）


####  how to load 

 start with gateway on call OkexfGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.okexf import OkexfGateway
main_engine.add_gateway(OkexfGateway)
```

&nbsp;


####  related fields 

- API hi钥 ：API Key
-  cryptographic key ：Secret Key
-  sessions ：3
-  password ：passphrase
-  lever ：Leverage
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 in OKEX official cape households and can get back into gold API access rights . 


&nbsp;

###  fire currency (HUOBI)

####  how to load 

 start with gateway on call HuobiGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.huobi import HuobiGateway
main_engine.add_gateway(HuobiGateway)
```

&nbsp;


####  related fields 

- API hi钥 ：API Key
-  cryptographic key ：Secret Key
-  sessions ：3
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 fire official cape households in the currency and gold can get back into the API access rights . 


&nbsp;



###  fire currency contracts (HBDM)

####  how to load 

 start with gateway on call HbdmGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.hbdm import HbdmGateway
main_engine.add_gateway(HbdmGateway)
```

&nbsp;


####  related fields 

- API hi钥 ：API Key
-  cryptographic key ：Secret Key
-  sessions ：3
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 fire official cape households in the currency and gold can get back into the API access rights . 


&nbsp;

### BITFINEX

####  how to load 

 start with gateway on call BitFinexGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.bitfinex import BitfinexGateway
main_engine.add_gateway(BitfinexGateway)
```

&nbsp;


####  related fields 

-  user ID：ID
-  password ：Secret
-  sessions ：3
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 in BITFINEX official cape households and can get back into gold API access rights . 



&nbsp;


### ONETOKEN

####  how to load 

 start with gateway on call OnetokenGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.onetoken import OnetokenGateway
main_engine.add_gateway(OnetokenGateway)
```

&nbsp;


####  related fields 

- Key hi钥 ：OT Key
-  cryptographic key ：OT Secret
-  sessions ：3
-  exchange ：["BINANCE", "BITMEX", "OKEX", "OKEF", "HUOBIP", "HUOBIF"]
-  account number ：
-  proxy address ：
-  proxy port ：



&nbsp;


####  account acquisition 

 in Onetoken official cape households and can get back into gold API access rights . 



&nbsp;

&nbsp;

### BINANCE

####  how to load 

 start with gateway on call BinanceGateway class ； then add_gateway() function to the main_engine on . 
```
from vnpy.gateway.binance import BinanceGateway
main_engine.add_gateway(BinanceGateway)
```

&nbsp;


####  related fields 

- Key hi钥 
- secret
- session_number( sessions )：3
- proxy_host
- proxy_port

&nbsp;


####  account acquisition 

 in BINANCE official cape households and can get back into gold API access rights . 

&nbsp;


### RPC

####  how to load 

RPC load it comes to service and client 
-  server ： run vntrader when loading rpc_service module 
    ```
    from vnpy.app.rpc_service import RpcService
    ```
     start up vntrader rear ， first connect external trade transactions such as CTP， then click on the menu bar " features "->"RPC service "， click on " start up "
-  client ： run vntrader when loading RpcGateway
    ```
    from vnpy.gateway.rpc import RpcGateway
    ```
     start up vntrader rear ， connection rpc interface to . 

####  related fields 
 service and client ， use the default parameters can be completed 

####  account acquisition 
 use rpc no additional application account ， account requires only an external interface 

####  other features 
rpc support the same external interface data distribution in the local multi-process ， for example, in the server connected ctp interface ， subscribed rb1910 rear ， the client will automatically subscribe to multiple processes subscription data from the server distribution #  trading interface 
