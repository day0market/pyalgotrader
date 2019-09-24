# Basic use


## starting program

### Graphics mode
LandedVN StationRear，Click onVN Trade LiteQuick access toVN Trader（onlyCTPinterface）；Or clickVN Trader ProFirst select underlying interface and the upper layer application as shown below，Re-entryVN Trader。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/VnTrader_Pro.png "enter image title here")



### Script mode

In the Folderexample\traderFoundrun.pyfile(NovnstudioUnder the，NeedgithubOn a separate download）。Press and hold“Shift” + Right into thecmdwindow，Enter the following command to enter FIG.VN Trader
```
python run.py 
```
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/Vntrader.PNG "enter image title here")

&nbsp;

## Connection interface
### SimNowsimulation

WithSinNowSimulation trading account loginCTPInterface as an example：Click on the menu bar“system”->“connectionCTP”Rear，As shown in FIG popCTPInterface configuration dialog，You can log the following entries：
- usernameusername：111111 （6Bit digital-only account）
- passwordpassword：1111111  （We need to change the password for a late test）
- Broker No.brokerid：9999 （SimNowThe default number Brokers）
- Transaction Server Addresstd_address：218.202.237.33 :10102 （Intraday test）
- Quotes server addressmd_address：218.202.237.33 :10112 （Intraday test）
- Authorization codeauth_code：0000000000000000（16More0）
- nameapp_id：simnow_client_test

After a successful connection，Log component outputs immediately successful land-related information，Users can also see account information，Position information，Contract and other related information query。

&nbsp;

## Subscribe Quotes
In exchange transaction component input codes and contracts，And press“Enter”Key to the subscriber market。Such as subscriptionsIFStock index futures，Exchange：CFFEX，name：IF905；Iron ore futures，Exchange：DCE，name：i1905。

At this point the market component displays the latest market information；Trading component will display the name of the contract，Quotes and display depth below：Such as the latest price、Buy a price、Sell ​​a price。（Digital currency market varieties can show a ten speed）

note：Fill in the subscription market code format can be made in the menu bar”help“->“Query contract”Found in
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/subcribe_contract.png "enter image title here")



&nbsp;

## Escrow
Transaction component for manual trading。In addition to the exchange and contract code entered in the stock market subscription，Also you need to fill the following5Fields：Principal direction、Open open type、Delegate type、Order price and quantity commission。（If the delegate type as market orders，Order price not fill。）

By placing an order at the same time commissioned local cache information，And to display the trusted component and an active component，Its status as a delegate“submitting”，Then wait for the commission in return。

Exchange received a delegation sent by the user，Insert it into the central order book to be brokered transactions，And push delegate return to the user：
- If the commission has not yet deal，Principal component and an active component will only update the time and commissioned two state field，Commissioned by the state to become“Unsold”；
- If the commission immediately deal，Entrusted to the relevant information will be removed from the active component，Add components to deal，Commissioned by the state to become“All transactions”。




&nbsp;

## Data monitoring

Data monitoring consists of the following components，And comes2Auxiliary function：Selected one of the following components，Right mouse button to select“Column Width”（Especially suitable for low screen resolution），Or choose“save data”（csvformat）

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/2_optiones.png "enter image title here")


### Quotes components
Subscribe for real-time monitoring of the stock market，As shown below，Monitor the content can be divided into3class：

- Contract Information：Contracts Code、Exchange、Name of Contract

- Market information：Latest price、Volume、Opening price、Highest Price、Lowest、Closing price、Buy a price、Buy a quantity、Sell ​​a price、Sell ​​a quantity

- other information：Time data push、interface

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/subcribe_contract_module.png "enter image title here")


### Active components
Principal activities Components of the transaction has not been used to store，Such as limit orders or market orders not immediately deal，Commissioned by the state is always“submitting”。In this double-clicking any component in a complete cancellation operation can delegate。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/active_order.png "enter image title here")

### Components deal
Components used to store transaction deal has been commissioned，requires attention3Field information：price、Quantity、time。They are pushing up the exchange of transaction information，Rather than request information。

note：Some interfaces will push independent transaction information，Such asCTPinterface；Some interfaces will need to request information from which to extract transaction related field，Such asTigerinterface。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/trade.png "enter image title here")



### Principal Components
Principal components used to store all of the delegation information issued by the user，It can be submitted to the state commission、Revoked、Part of the transaction、All transactions、And so refused to single。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/order.png "enter image title here")


### Component positions
Components used to record the history of their positions positions。Where the need to understand the meaning of the following fields
- direction：Futures varieties with long and short direction；The stock varieties direction“net”Positions。
- Yesterday warehouse：Which appears on the derived level of this specific、Need flat yesterday Mode
- Quantity：Total positions，Now the warehouse + Yesterday warehouse
- Average price：The average transaction price history（Some giant commissioned，Part of the transaction will occur repeatedly，We need to calculate the average price）
- Profit and loss：Profit and loss positions：Multi-warehouse case，profit = Current price - Average price；Short positions and vice versa。
  
If leave open，Clear the number of positions，Floating profit and loss became actual profit and loss account balances to affect change。Therefore, the following fields：Quantity、Yesterday warehouse、freeze、Average price、Profit and loss are“0”，As shown below。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/query_position.png "enter image title here")

### Components funds
Funding component displays the basic information account，Note that the figure below3Field information：
- Available funds：Cash can be used to delegate
- freeze：Entrusted operation amount frozen（The margin is not a concept）
- Balance：Total funds，To use funds + Security deposit + Floating profit and loss 

note：If all positions，Floating profit and loss became actual profit and loss，Margin and floating profit and loss cleared，Equal to the total available funds of funds

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/query_account.png "enter image title here")



### Log component
Log component is used to display interface login information as well as being given the information commission，As shown below。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/write_log.png "enter image title here")



&nbsp;

## Application Module

vn.pyOfficial provides a quantitative trading application module out of the box，In the menu bar“Features”，Application module is displayed，As shown below：

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/application.png "enter image title here")

&nbsp;

## Global Configuration

In the menu bar“Configuration”，Can be configured globally：Such as configurationGUIInterface font size，Types of，Database species，RQDataAccount password（It used to initializeRQDataClient，Download History，Or loading data from disk to initialize Policy），Set upemailTo send a message。

itsemailThe settings are as follows：
email.server: SMTPMail server address
email.port: SMTPMail server port number
email.username: E-mail user name
email.password: email Password
email.sender: Sender E-mail
email.receiver: E-mail recipient

