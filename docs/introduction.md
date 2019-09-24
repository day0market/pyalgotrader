# Features

As a basisPythonThe quantitative trading development framework，vn.pyWe are committed to providing the transactionAPIFor a complete solution to the automated trading strategies。

## Target users

If there is less demand，Give it a tryvn.py：

* based onPythonLanguage to develop their own quantitative trading program，Take advantage ofPythonCommunities powerful data and machine learning research ecology
* Through a set of standardized trading platform system，Butt of many different types of domestic financial markets：Securities、futures、Options、Exchange、Digital currency
* After full use of quantitative testing firm policy engine，To complete the data maintenance、Strategy Development、Backtesting study to the entire business process automated trading firm
* Platform for a variety of custom extensions，To meet the needs of individual transactions：Increase transaction interface，modifyGUIgraphic interface，Development of complex application-based event-driven engine strategy
* Control of all source code program trading details，The complete elimination of all kinds of backdoors，Avoid stolen Policy、Intercepted trading signals、Steal account passwords and other risks
* To save money to pay the cost of quantitative trading platform，You do not have to spend tens of thousands of annual software license fees or extra point of each transaction


## Scenarios

From a professional individual investors、Entrepreneurial Private，The brokerage and information management department、Currency ringToken Fund，Can be foundvn.pyApplication scenarios。

* Professional individual investors：useVN TraderDirect Futures CompanyCTPFutures counter，From strategy to achieve the full development of automated trading firm offer completeCTABusiness Process
* Entrepreneurial Private：based onRpcServiceBuild server-side unified offer channel，It allows traders to develop their own local PC application of various types of trading strategies
* Brokerage and information management department：Docking securities company's unified deploymentO32Information management system，Custom development of complex systems-based multi-strategy event-driven engine
* Currency ringToken Fund：useVN TraderConnecting multiple currency exchange rings，byAlgoTradingAlgorithmic trading module to automate entrusted to the Executive，Reduce the cost impact


## Supported Interface

**vnpy.gateway**，Cover domestic and foreign varieties of all transactions transaction interface：

* Domestic market

  * CTP(ctp)：Domestic futures、Options

  * CTP Mini(mini)：Domestic futures、Options

  * Pegasus(femas)：Domestic futures

  * Core Width(oes)：Domestic securities（Ashare）

  * NakaYasushiXTP(xtp)：Domestic securities（Ashare）

  * 华鑫奇 point(tora)：Domestic securities（Ashare）

* overseas market
    
  * Fu passers securities(futu)：Hong Kong stocks、US stocks

  * Tiger Securities(tiger)：Global Securities、futures、Options、Foreign exchange

  * Interactive Brokers(ib)：Global Securities、futures、Options、Foreign exchange

  * Yi Sheng9.0External disk(tap)：Global Futures

* Digital Currency

  * BitMEX(bitmex)：Digital currency futures、Options、Sustainable contracts

  * OKEXcontract(okexf)：Digital currency futures

  * Fire currency contracts(hbdm)：Digital currency futures

  * An coins(binance)：Digital currency spot

  * OKEX(okex)：Digital currency spot

  * Fire currency(huobi)：Digital currency spot

  * Bitfinex(bitfinex)：Digital currency spot

  * 1Token(onetoken)：Digital currency broker（Stock、futures）

* Special Applications

  * RPCservice(rpc)：Cross-process communication interface，For distributed architecture


## Supported applications

**vnpy.app**，All kinds of quantitative strategies trading applications out of the box：

* cta_strategy：CTAPolicy engine module，While maintaining the ease of use，To allow for usersCTAProcess class policy to run in the report commissioned by the withdrawal behavior of fine-grained control（Reduce transaction Slippage、High frequency strategies）

* cta_backtester：CTAStrategy Backtesting module，Without the use ofJupyter Notebook，Direct use graphical interface directly strategy backtesting analysis、Parameter optimization and other related work

* algo_trading：Algorithmic trading module，It offers a variety of commonly used smart trading algorithms：TWAP、Sniper、Iceberg、BestLimitand many more，Support for common algorithm configuration is saved

* script_trader：Scripts policy module，For multi-target combination class trading strategy design，At the same time can also be implemented directly on the command lineREPLInstruction in the form of transaction，Backtesting feature is not supported

* rpc_service：RPCService Module，Allows aVN TraderProcess starts for the server，As a unified market and transaction routing channel，It allows multiple simultaneous client connections，Multi-process distributed systems

* csv_loader：CSVHistorical Data Loader，For loadingCSVHistorical data format file into the database platform，Backtesting for strategy and research firm initialization function，Support for custom data format header

* data_recorder：Quotes recording module，Be configured based graphical interface，According to the needs of real-time recordingTickorKQuotes line into the database，Backtesting for strategy or firm initialization

* risk_manager：Risk Management Module，Including transaction provides flow control、Under a single number、Principal activities、Statistics and limit the total number of regular withdrawals，Effective to achieve the control function of the front end of the wind



## General class components

**vnpy.api**，PythontransactionAPIInterface Package，The deal provides an interface to achieve the underlying docking。

**vnpy.event**，Simple and easy to use event-driven engine，As the core of event-driven trading programs。

**vnpy.rpc**，Inter-process communication standard components，System implementation for complex transactions distributed deployment。

**vnpy.chart**，Pythonhigh performanceKLine chart，Support large amount of data in the chart display and real-time data updates。
