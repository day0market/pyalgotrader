# Trading Interface

## How to Connect

FromgatewayFolder on the introduction of the interface program，byadd_gateway()Function mobilize，The final show to the graphical user interfaceVN Traderin。

In the menu bar"system"->"connectionCTP”Button will pop up as account configuration window，Enter the account number、Passwords and other information that is relevant connection interface，And immediately carry out inquiries: Such as query account information、Queries positions、Information inquiry commission、Query transaction information。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/gateway/login.png)

&nbsp;

### Load interface needs with

Example charging interface in the root directory"tests\trader"Folderrun.pyFile。
- FromgatewayThe introduction of file folders interface class，Such asfrom vnpy.gateway.ctp import CtpGateway;
- And by creating an event engine objectadd_gateway()Add function interface program;
- Creating graphical objectsmain_window，WithVN TraderInterface show up。


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


### Configuration and connection

turn oncmdwindow，Use the command“Python run.py"To enterVN TraderUser interface。Click on the top left of the menu bar"system"->"connectionCTP”Button configuration window will pop account，Enter the account number、Passwords and other information that is relevant connection interface。

Process connection interface is first initialized account information，Then callconnet()Function to connect the port and market trading port。
- Trading port：Query user information（As account funds、Positions、Commissioned record、Transaction Record）、Queries can be traded contract information、Hanging cancellation operation；
- Quotes port：Subscribe to receive stock market information push、Receiving a user-related information（Such as account money to upgrade、Position Update、Push commission、Push deal）Update callback push。


&nbsp;


### modifyjsonProfiles

Related stored in interface configurationjsonFile，In FigureCUnder disk user directory.vntraderFolder。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/gateway/.vntrader.png)

So you want to modify the interface configuration file，I.e., the user interface may be a graphicalVN TraderIn the modification，Can also directly in.vntradermodifyjsonfile。
In addition tojsonProfile separate fromvnpyBenefit is：Avoid each upgrade must be reconfiguredjsonfile。


&nbsp;


### View tradable contracts

Interface login first，Then click on the menu bar"help"->"Query contract”Button blank“Query contract”window。Click on“Inquire”Button will display the query results，Figure。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/gateway/query_contract.png)



&nbsp;

## Interface Category

| interface     |                    Types of                    |
| -------- | :----------------------------------------: |
| CTP      |                    futures                    |
| MINI     |                    futures                    |
| FEMAS    |                    futures                    |
| XTP      | Domestic stock、index、fund、Bond、Options、Margin |
| OES      |                  Domestic stock                  |
| TORA     |                  Domestic stock                  |
| IB       |            External disk stock、futures、Options            |
| TAP      |               External disk futures、Options               |
| FUTU     |            Domestic stock、Hong Kong stocks、US stocks            |
| TIGER    |            Domestic stock、Hong Kong stocks、US stocks            |
| ALPACA   |                    US stocks                    |
| BITFINEX |                  Digital Currency                  |
| BITMEX   |                  Digital Currency                  |
| BINANCE  |                  Digital Currency                  |
| OKEX     |                  Digital Currency                  |
| OKEXF    |                  Digital Currency                  |
| HUOBI    |                  Digital Currency                  |
| HBDM     |                  Digital Currency                  |
| ONETOKEN |                  Digital Currency                  |
| RPC      |                  RPCservice                   |



&nbsp;


## Detailed Interface

### CTP

#### How to Load

run.pyDocument provides the interface load sample：Start withgatewayOn callctpGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.ctp import CtpGateway
main_engine.add_gateway(CtpGateway)
```

&nbsp;

#### Related Fields

- username：username
- password：password：
- Broker No.：brokerid
- Transaction Server Address：td_address
- Quotes server address：md_address
- product name：product_info
- Authorized coding：auth_code
  
&nbsp;

#### Account acquisition

- Simulation account：FromSimNowGet on the site。Simply enter the phone number and the SMS verification can be。（SMS verification sometimes can only receive normal working hours on weekdays）SimNowThe user name6Pure digital bits，Broker No.9999，And provide2Environmental simulation test suite for intraday trading and after-hours。
  
- Firm account：In the futures company account，Can be opened by contacting customer manager。A user named Pure Digital，Brokers also a number4Pure digital bits。（Each futures broker's numbers are different）Other，A firm offer trading accounts can be opened emulation function，Also you need to contact customer manager。


&nbsp;

### MINI

#### How to Load

Start withgatewayOn callMiniGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.mini import MiniGateway
main_engine.add_gateway(MiniGateway)
```

&nbsp;

#### Related Fields

- username：username
- password：password：
- Broker No.：brokerid
- Transaction Server Address：td_address
- Quotes server address：md_address
- product name：product_info
- Authorized coding：auth_code
  
&nbsp;

#### Account acquisition

In the futures company account，Can be opened by contacting customer manager。A user named Pure Digital，Brokers also a number4Pure digital bits。（Each futures broker's numbers are different）Other，A firm offer trading accounts can be opened emulation function，Also you need to contact customer manager。


&nbsp;

### Pegasus（FEMAS）

#### How to Load

Start withgatewayOn callFemasGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.femas import FemasGateway
main_engine.add_gateway(FemasGateway)
```

&nbsp;

#### Related Fields

- username：username
- password：password：
- Broker No.：brokerid
- Transaction Server Address：td_address
- Quotes server address：md_address
- product name：product_info
- Authorized coding：auth_code
  
&nbsp;

#### Account acquisition

In the futures company account，Can be opened by contacting customer manager。A user named Pure Digital，Brokers also a number4Pure digital bits。（Each futures broker's numbers are different）Other，A firm offer trading accounts can be opened emulation function，Also you need to contact customer manager。


&nbsp;



### Counter in Thailand(XTP)

#### How to Load

Start withgatewayOn callXtpGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.xtp import XtpGateway
main_engine.add_gateway(XtpGateway)
```

&nbsp;


#### Related Fields

- account number：
- password：
- client number": 1
- Quotes address：
- Quotes port": 0
- Trading Address：
- Trading port": 0
- Quotes agreement: ["TCP", "UDP"]
- Authorization code：

&nbsp;


#### Account acquisition

Test account please contact the Thai Securities and application。

#### Other features

XTPIt is the first to provide the margin of speed counter。

&nbsp;


### Wide Rui counter(OES)

#### How to Load

Start withgatewayOn callOesGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.oes import OesGateway
main_engine.add_gateway(OesGateway)
```

&nbsp;


#### Related Fields

- username：username
- password：password
- Hard disk serial number：hdd_serial
- Trading commission Server：td_ord_server
- Transaction server returns：td_rpt_server
- Trading query server：td_qry_server
- Quotes push server：md_tcp_server
- Quotes query server：md_qry_server

&nbsp;


#### Account acquisition

Wide test account please contact Core Technology Application

&nbsp;

#### Other features

Rui counter offer wide networkUDPLow-latency multicast quotes and real-time transaction information push。

&nbsp;


### 华鑫奇 point(TORA)

#### How to Load

Start withgatewayOn callToraGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.tota import ToraGateway
main_engine.add_gateway(OesGateway)
```

&nbsp;

#### Related Fields

- account number: username
- password: password
- Transaction Server: td_address
- Quotes server: md_address

&nbsp;

#### Account acquisition

Test account please contact Huaxin Securities application


&nbsp;

### Interactive Brokers(IB)

#### How to Load

Start withgatewayOn callIbGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.ib import IbGateway
main_engine.add_gateway(IbGateway)
```

&nbsp;


#### Related Fields

- TWSaddress：127.0.0.1
- TWSport：7497
- client number：1


&nbsp;


#### Account acquisition

Available at Interactive Brokers account and deposit afterAPIAccess rights。It has a firm offer to open an account before they can apply for mock trading account。

&nbsp;

#### Other features

Tradable varieties almost global coverage of stock、Options、Options；Relatively low fees。

noteIBContract interface code more special，Go to the official website of the sector inquiry Product inquiry，VN TraderUse Interactive Brokers is a unique identifier for each contract at a certain exchangeConIdAs Contract Code，Rather thanSymbolorLocalName。

&nbsp;


### Yi Sheng external disk(TAP)

#### How to Load

Start withgatewayOn callTapGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.tap import TapGateway
main_engine.add_gateway(TapGateway)
```

&nbsp;


#### Related Fields

- Authorization code：auth code
- Quotes account：quote username
- Quotes password：quote password
- Quotes address：123.15.58.21
- Quotes port：7171



&nbsp;


#### Account acquisition

inTAPAfter the deposit to open an account and getAPIAccess rights。

&nbsp;


### Fu passers securities(FUTU)

#### How to Load

Start withgatewayOn callFutuGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.futu import FutuGateway
main_engine.add_gateway(FutuGateway)
```

&nbsp;


#### Related Fields

- address：127.0.0.1
- password：
- port：11111
- market：HK or US
- surroundings：TrdEnv.REAL or TrdEnv.SIMULATE


&nbsp;


#### Account acquisition

Rich in transit securities account and can get back into goldAPIAccess rights。It has a firm offer to open an account before they can apply for mock trading account。






&nbsp;

### Tiger Securities(TIGER)


#### How to Load

Start withgatewayOn callTigerGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.tiger import TigerGateway
main_engine.add_gateway(TigerGateway)
```

&nbsp;


#### Related Fields

- userID：tiger_id
- Global Account：account
- Standard account：standard_account
- Hi钥：private_key



&nbsp;


#### Account acquisition

Tiger securities account and can get back into goldAPIAccess rights。It has a firm offer to open an account before they can apply for mock trading account。


&nbsp;


### ALPACA

#### How to Load
Start withgatewayOn callAlpacaGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.alpaca import AlpacaGateway
main_engine.add_gateway(AlpacaGateway)
```

&nbsp;

#### Related Fields
- KEY ID: key
- Secret Key: secret
- Sessions: 10
- server:["REAL", "PAPER"]
#### Account acquisition
inOKEXOfficial CAPE households and can get back into goldAPIAccess rights。
#### Other features

&nbsp;


### BITMEX

#### How to Load

Start withgatewayOn callBitmexGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.bitmex import BitmexGateway
main_engine.add_gateway(BitmexGateway)
```

&nbsp;


#### Related Fields

- userID：ID
- password：Secret
- Sessions：3
- server：REAL or TESTNET
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

inBITMEXOfficial CAPE households and can get back into goldAPIAccess rights。



&nbsp;

### OKEXStock（OKEX）


#### How to Load

Start withgatewayOn callOkexGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.okex import OkexGateway
main_engine.add_gateway(OkexGateway)
```

&nbsp;


#### Related Fields

- APIHi钥：API Key
- Cryptographic key：Secret Key
- Sessions：3
- password：passphrase
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

inOKEXOfficial CAPE households and can get back into goldAPIAccess rights。



&nbsp;


### OKEXfutures（OKEXF）


#### How to Load

Start withgatewayOn callOkexfGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.okexf import OkexfGateway
main_engine.add_gateway(OkexfGateway)
```

&nbsp;


#### Related Fields

- APIHi钥：API Key
- Cryptographic key：Secret Key
- Sessions：3
- password：passphrase
- lever：Leverage
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

inOKEXOfficial CAPE households and can get back into goldAPIAccess rights。


&nbsp;

### Fire currency(HUOBI)

#### How to Load

Start withgatewayOn callHuobiGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.huobi import HuobiGateway
main_engine.add_gateway(HuobiGateway)
```

&nbsp;


#### Related Fields

- APIHi钥：API Key
- Cryptographic key：Secret Key
- Sessions：3
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

Fire official CAPE households in the currency and gold can get back into theAPIAccess rights。


&nbsp;



### Fire currency contracts(HBDM)

#### How to Load

Start withgatewayOn callHbdmGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.hbdm import HbdmGateway
main_engine.add_gateway(HbdmGateway)
```

&nbsp;


#### Related Fields

- APIHi钥：API Key
- Cryptographic key：Secret Key
- Sessions：3
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

Fire official CAPE households in the currency and gold can get back into theAPIAccess rights。


&nbsp;

### BITFINEX

#### How to Load

Start withgatewayOn callBitFinexGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.bitfinex import BitfinexGateway
main_engine.add_gateway(BitfinexGateway)
```

&nbsp;


#### Related Fields

- userID：ID
- password：Secret
- Sessions：3
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

inBITFINEXOfficial CAPE households and can get back into goldAPIAccess rights。



&nbsp;


### ONETOKEN

#### How to Load

Start withgatewayOn callOnetokenGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.onetoken import OnetokenGateway
main_engine.add_gateway(OnetokenGateway)
```

&nbsp;


#### Related Fields

- KeyHi钥：OT Key
- Cryptographic key：OT Secret
- Sessions：3
- Exchange：["BINANCE", "BITMEX", "OKEX", "OKEF", "HUOBIP", "HUOBIF"]
- account number：
- Proxy Address：
- Proxy Port：



&nbsp;


#### Account acquisition

inOnetokenOfficial CAPE households and can get back into goldAPIAccess rights。



&nbsp;

&nbsp;

### BINANCE

#### How to Load

Start withgatewayOn callBinanceGatewayclass；Thenadd_gateway()Function to themain_engineon。
```
from vnpy.gateway.binance import BinanceGateway
main_engine.add_gateway(BinanceGateway)
```

&nbsp;


#### Related Fields

- KeyHi钥
- secret
- session_number(Sessions)：3
- proxy_host
- proxy_port

&nbsp;


#### Account acquisition

inBINANCEOfficial CAPE households and can get back into goldAPIAccess rights。

&nbsp;


### RPC

#### How to Load

RPCLoad it comes to service and client
- Server：runvntraderWhen loadingrpc_serviceModule
    ```
    from vnpy.app.rpc_service import RpcService
    ```
    start upvntraderRear，First connect external trade transactions such asCTP，Then click on the menu bar"Features"->"RPCservice"，Click on"start up"
- Client：runvntraderWhen loadingRpcGateway
    ```
    from vnpy.gateway.rpc import RpcGateway
    ```
    start upvntraderRear，connectionrpcInterface to。

#### Related Fields
Service and client，Use the default parameters can be completed

#### Account acquisition
userpcNo additional application account，Account requires only an external interface

#### Other features
rpcSupport the same external interface data distribution in the local multi-process，For example, in the server connectedctpinterface，Subscribedrb1910Rear，The client will automatically subscribe to multiple processes subscription data from the server distribution# Trading Interface
