#  features 

 as a basis Python the quantitative trading development framework ，vn.py we are committed to providing the transaction API for a complete solution to the automated trading strategies . 

##  target users 

 if there is less demand ， give it a try vn.py：

*  based on Python language to develop their own quantitative trading program ， take advantage of Python communities powerful data and machine learning research ecology 
*  through a set of standardized trading platform system ， butt of many different types of domestic financial markets ： securities ,  futures ,  options ,  exchange ,  digital currency 
*  after full use of quantitative testing firm policy engine ， to complete the data maintenance ,  strategy development ,  backtesting study to the entire business process automated trading firm 
*  platform for a variety of custom extensions ， to meet the needs of individual transactions ： increase transaction interface ， modify GUI graphic interface ， development of complex application-based event-driven engine strategy 
*  control of all source code program trading details ， the complete elimination of all kinds of backdoors ， avoid stolen policy ,  intercepted trading signals ,  steal account passwords and other risks 
*  to save money to pay the cost of quantitative trading platform ， you do not have to spend tens of thousands of annual software license fees or extra point of each transaction 


##  scenarios 

 from a professional individual investors ,  entrepreneurial private ， the brokerage and information management department ,  currency ring Token Fund， can be found vn.py application scenarios . 

*  professional individual investors ： use VN Trader direct futures company CTP futures counter ， from strategy to achieve the full development of automated trading firm offer complete CTA business process 
*  entrepreneurial private ： based on RpcService build server-side unified offer channel ， it allows traders to develop their own local pc application of various types of trading strategies 
*  brokerage and information management department ： docking securities company's unified deployment O32 information management system ， custom development of complex systems-based multi-strategy event-driven engine 
*  currency ring Token Fund： use VN Trader connecting multiple currency exchange rings ， by AlgoTrading algorithmic trading module to automate entrusted to the executive ， reduce the cost impact 


##  supported interface 

**vnpy.gateway**， cover domestic and foreign varieties of all transactions transaction interface ：

*  domestic market 

  * CTP(ctp)： domestic futures ,  options 

  * CTP Mini(mini)： domestic futures ,  options 

  *  pegasus (femas)： domestic futures 

  *  core width (oes)： domestic securities （A share ）

  *  nakayasushi XTP(xtp)： domestic securities （A share ）

  *  华鑫奇 point (tora)： domestic securities （A share ）

*  overseas market 
    
  *  fu passers securities (futu)： hong kong stocks ,  us stocks 

  *  tiger securities (tiger)： global securities ,  futures ,  options ,  foreign exchange 

  * Interactive Brokers(ib)： global securities ,  futures ,  options ,  foreign exchange 

  *  yi sheng 9.0 external disk (tap)： global futures 

*  digital currency 

  * BitMEX(bitmex)： digital currency futures ,  options ,  sustainable contracts 

  * OKEX contract (okexf)： digital currency futures 

  *  fire currency contracts (hbdm)： digital currency futures 

  *  an coins (binance)： digital currency spot 

  * OKEX(okex)： digital currency spot 

  *  fire currency (huobi)： digital currency spot 

  * Bitfinex(bitfinex)： digital currency spot 

  * 1Token(onetoken)： digital currency broker （ stock ,  futures ）

*  special applications 

  * RPC service (rpc)： cross-process communication interface ， for distributed architecture 


##  supported applications 

**vnpy.app**， all kinds of quantitative strategies trading applications out of the box ：

* cta_strategy：CTA policy engine module ， while maintaining the ease of use ， to allow for users CTA process class policy to run in the report commissioned by the withdrawal behavior of fine-grained control （ reduce transaction slippage ,  high frequency strategies ）

* cta_backtester：CTA strategy backtesting module ， without the use of Jupyter Notebook， direct use graphical interface directly strategy backtesting analysis ,  parameter optimization and other related work 

* algo_trading： algorithmic trading module ， it offers a variety of commonly used smart trading algorithms ：TWAP, Sniper, Iceberg, BestLimit and many more ， support for common algorithm configuration is saved 

* script_trader： scripts policy module ， for multi-target combination class trading strategy design ， at the same time can also be implemented directly on the command line REPL instruction in the form of transaction ， backtesting feature is not supported 

* rpc_service：RPC service module ， allows a VN Trader process starts for the server ， as a unified market and transaction routing channel ， it allows multiple simultaneous client connections ， multi-process distributed systems 

* csv_loader：CSV historical data loader ， for loading CSV historical data format file into the database platform ， backtesting for strategy and research firm initialization function ， support for custom data format header 

* data_recorder： quotes recording module ， be configured based graphical interface ， according to the needs of real-time recording Tick or K quotes line into the database ， backtesting for strategy or firm initialization 

* risk_manager： risk management module ， including transaction provides flow control ,  under a single number ,  principal activities ,  statistics and limit the total number of regular withdrawals ， effective to achieve the control function of the front end of the wind 



##  general class components 

**vnpy.api**，Python transaction API interface package ， the deal provides an interface to achieve the underlying docking . 

**vnpy.event**， simple and easy to use event-driven engine ， as the core of event-driven trading programs . 

**vnpy.rpc**， inter-process communication standard components ， system implementation for complex transactions distributed deployment . 

**vnpy.chart**，Python high performance K line chart ， support large amount of data in the chart display and real-time data updates . 
