# Transaction risk control

Transaction risk control module belonging to ex ante risk control，That is commissioned in transactionsAPIInterface sent out before，Check the status need not exceed the limit wind control，These include：
- It must be greater than the number of commission0
- The maximum number of single delegate
- The maximum number of total turnover of the day
- Commissioned by the maximum number of streams
- The maximum number of currently active delegate
- Day maximum number of withdrawals

&nbsp;

## Load Startup

enterVN TraderRear，First landing Interface，The connectionCTP；Then click on the menu bar“Features”->"Transaction risk control“Rear，Transaction risk control window will pop up，Figure。
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/risk_manager/risk_manager.png)

Parameter display window，It corresponds toC:\Users\Administrator\.vntraderinsiderisk_manager_setting.jsonThe parameters dictionary，Figure。
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/risk_manager/data_setting.png)

in“Wind control operating status”Click the selection box“start up”Rear
- Immediately callRiskManagerEngineCategoryupdate_setting()Function readsrisk_manager_setting.jsonThe parameters dictionary and the binding properties of the class。
- Output in the log"Transaction risk control function is activated"。
- runcheck_risk()function，To examine every issue to a sum of commission meets the requirements of a variety of risk control，If after all meet，Flow control count+1，Commissioned by realAPIInterface to send out。

&nbsp;

## Change parameters

Transaction risk control component allows users to modify risk control parameters。due toGUIEach interface is based on the parameter fieldPyQt5ofQSpinBox，Users can click with the mouse up and down arrows to modify，You can also directly modify keyboard input。

Finally, click on the bottom of the window“Storage”Push button，To callRiskManagerEngineCategorysave_setting()Function to update torisk_manager_setting.jsonThe parameters dictionary，Finally,update_setting()The function is bound to the dictionary parameter attribute class。

&nbsp;

## Stop wind control

in“Wind control operating status”Click the selection box“Stopped”Rear，RiskManagerEngineCategoryactivebecomeFalse，check_risk()Check function no longer control the wind flow control status commissioned，While the output in the log"Transaction risk control function stop"。

