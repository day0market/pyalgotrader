#  basic use 


##  starting program 

###  graphics mode 
 landed VN Station rear ， click on VN Trade Lite quick access to VN Trader（ only CTP interface ）； or click VN Trader Pro first select underlying interface and the upper layer application as shown below ， re-entry VN Trader. 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/VnTrader_Pro.png "enter image title here")



###  script mode 

 in the folder example\trader found run.py file ( no vnstudio under the ， need github on a separate download ）.  press and hold “Shift” +  right into the cmd window ， enter the following command to enter fig. VN Trader
```
python run.py 
```
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/Vntrader.PNG "enter image title here")

&nbsp;

##  connection interface 
### SimNow simulation 

 with SinNow simulation trading account login CTP interface as an example ： click on the menu bar “ system ”->“ connection CTP” rear ， as shown in fig pop CTP interface configuration dialog ， you can log the following entries ：
-  username username：111111 （6 bit digital-only account ）
-  password password：1111111  （ we need to change the password for a late test ）
-  broker no. brokerid：9999 （SimNow the default number brokers ）
-  transaction server address td_address：218.202.237.33 :10102 （ intraday test ）
-  quotes server address md_address：218.202.237.33 :10112 （ intraday test ）
-  authorization code auth_code：0000000000000000（16 more 0）
-  name app_id：simnow_client_test

 after a successful connection ， log component outputs immediately successful land-related information ， users can also see account information ， position information ， contract and other related information query . 

&nbsp;

##  subscribe quotes 
 in exchange transaction component input codes and contracts ， and press “Enter” key to the subscriber market .  such as subscriptions IF stock index futures ， exchange ：CFFEX， name ：IF905； iron ore futures ， exchange ：DCE， name ：i1905. 

 at this point the market component displays the latest market information ； trading component will display the name of the contract ， quotes and display depth below ： such as the latest price ,  buy a price ,  sell ​​a price . （ digital currency market varieties can show a ten speed ）

 note ： fill in the subscription market code format can be made in the menu bar ” help “->“ query contract ” found in 
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/subcribe_contract.png "enter image title here")



&nbsp;

##  escrow 
 transaction component for manual trading .  in addition to the exchange and contract code entered in the stock market subscription ， also you need to fill the following 5 fields ： principal direction ,  open open type ,  delegate type ,  order price and quantity commission . （ if the delegate type as market orders ， order price not fill . ）

 by placing an order at the same time commissioned local cache information ， and to display the trusted component and an active component ， its status as a delegate “ submitting ”， then wait for the commission in return . 

 exchange received a delegation sent by the user ， insert it into the central order book to be brokered transactions ， and push delegate return to the user ：
-  if the commission has not yet deal ， principal component and an active component will only update the time and commissioned two state field ， commissioned by the state to become “ unsold ”；
-  if the commission immediately deal ， entrusted to the relevant information will be removed from the active component ， add components to deal ， commissioned by the state to become “ all transactions ”. 




&nbsp;

##  data monitoring 

 data monitoring consists of the following components ， and comes 2 auxiliary function ： selected one of the following components ， right mouse button to select “ column width ”（ especially suitable for low screen resolution ）， or choose “ save data ”（csv format ）

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/2_optiones.png "enter image title here")


###  quotes components 
 subscribe for real-time monitoring of the stock market ， as shown below ， monitor the content can be divided into 3 class ：

-  contract information ： contracts code ,  exchange ,  name of contract 

-  market information ： latest price ,  volume ,  opening price ,  highest price ,  lowest ,  closing price ,  buy a price ,  buy a quantity ,  sell ​​a price ,  sell ​​a quantity 

-  other information ： time data push ,  interface 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/subcribe_contract_module.png "enter image title here")


###  active components 
 principal activities components of the transaction has not been used to store ， such as limit orders or market orders not immediately deal ， commissioned by the state is always “ submitting ”.  in this double-clicking any component in a complete cancellation operation can delegate . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/active_order.png "enter image title here")

###  components deal 
 components used to store transaction deal has been commissioned ， requires attention 3 field information ： price ,  quantity ,  time .  they are pushing up the exchange of transaction information ， rather than request information . 

 note ： some interfaces will push independent transaction information ， such as CTP interface ； some interfaces will need to request information from which to extract transaction related field ， such as Tiger interface . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/trade.png "enter image title here")



###  principal components 
 principal components used to store all of the delegation information issued by the user ， it can be submitted to the state commission ,  revoked ,  part of the transaction ,  all transactions ,  and so refused to single . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/order.png "enter image title here")


###  component positions 
 components used to record the history of their positions positions .  where the need to understand the meaning of the following fields 
-  direction ： futures varieties with long and short direction ； the stock varieties direction “ net ” positions . 
-  yesterday warehouse ： which appears on the derived level of this specific ,  need flat yesterday mode 
-  quantity ： total positions ， now the warehouse  +  yesterday warehouse 
-  average price ： the average transaction price history （ some giant commissioned ， part of the transaction will occur repeatedly ， we need to calculate the average price ）
-  profit and loss ： profit and loss positions ： multi-warehouse case ， profit  =  current price  -  average price ； short positions and vice versa . 
  
 if leave open ， clear the number of positions ， floating profit and loss became actual profit and loss account balances to affect change .  therefore, the following fields ： quantity ,  yesterday warehouse ,  freeze ,  average price ,  profit and loss are “0”， as shown below . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/query_position.png "enter image title here")

###  components funds 
 funding component displays the basic information account ， note that the figure below 3 field information ：
-  available funds ： cash can be used to delegate 
-  freeze ： entrusted operation amount frozen （ the margin is not a concept ）
-  balance ： total funds ， to use funds  +  security deposit  +  floating profit and loss  

 note ： if all positions ， floating profit and loss became actual profit and loss ， margin and floating profit and loss cleared ， equal to the total available funds of funds 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/query_account.png "enter image title here")



###  log component 
 log component is used to display interface login information as well as being given the information commission ， as shown below . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/write_log.png "enter image title here")



&nbsp;

##  application module 

vn.py official provides a quantitative trading application module out of the box ， in the menu bar “ features ”， application module is displayed ， as shown below ：

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/application.png "enter image title here")

&nbsp;

##  global configuration 

 in the menu bar “ configuration ”， can be configured globally ： such as configuration GUI interface font size ， types of ， database species ，RQData account password （ it used to initialize RQData client ， download history ， or loading data from disk to initialize policy ）， set up email to send a message . 

 its email the settings are as follows ：
email.server: SMTP mail server address 
email.port: SMTP mail server port number 
email.username:  e-mail user name 
email.password:  email password 
email.sender:  sender e-mail 
email.receiver:  e-mail recipient 

