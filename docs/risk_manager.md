#  transaction risk control 

 transaction risk control module belonging to ex ante risk control ， that is commissioned in transactions API interface sent out before ， check the status need not exceed the limit wind control ， these include ：
-  it must be greater than the number of commission 0
-  the maximum number of single delegate 
-  the maximum number of total turnover of the day 
-  commissioned by the maximum number of streams 
-  the maximum number of currently active delegate 
-  day maximum number of withdrawals 

&nbsp;

##  load startup 

 enter VN Trader rear ， first landing interface ， the connection CTP； then click on the menu bar “ features ”->" transaction risk control “ rear ， transaction risk control window will pop up ， figure . 
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/risk_manager/risk_manager.png)

 parameter display window ， it corresponds to C:\Users\Administrator\.vntrader inside risk_manager_setting.json the parameters dictionary ， figure . 
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/risk_manager/data_setting.png)

 in “ wind control operating status ” click the selection box “ start up ” rear 
-  immediately call RiskManagerEngine category update_setting() function reads risk_manager_setting.json the parameters dictionary and the binding properties of the class . 
-  output in the log " transaction risk control function is activated ". 
-  run check_risk() function ， to examine every issue to a sum of commission meets the requirements of a variety of risk control ， if after all meet ， flow control count +1， commissioned by real API interface to send out . 

&nbsp;

##  change parameters 

 transaction risk control component allows users to modify risk control parameters .  due to GUI each interface is based on the parameter field PyQt5 of QSpinBox， users can click with the mouse up and down arrows to modify ， you can also directly modify keyboard input . 

 finally, click on the bottom of the window “ storage ” push button ， to call RiskManagerEngine category save_setting() function to update to risk_manager_setting.json the parameters dictionary ， finally, update_setting() the function is bound to the dictionary parameter attribute class . 

&nbsp;

##  stop wind control 

 in “ wind control operating status ” click the selection box “ stopped ” rear ，RiskManagerEngine category active become False，check_risk() check function no longer control the wind flow control status commissioned ， while the output in the log " transaction risk control function stop ". 

