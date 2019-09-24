# RPCservice
Global LockGILThe presence of leadPythonOnly useCPUMonocyte count of force。Shown its shortcomings single-process architecture in Figure：

![](https://static.vnpy.com/upload/temp/3f51a477-36db-41d4-9632-75067ba24be7.png)

Use multi-process distributed application architecture can break through the limit。But the data between each process，Default within the operating system is independently isolated，Can not directly access。
RPCService just to solve the pain points：RPCFull nameRemote-Procedure-Call，Chinese“Remote Procedure Call”，It is one of the most commonly used cross-process communication。invnpyin，A connected transaction interface acts as a specific processServercharacter of，Push-event in the local physical machine or internal LAN，Pushed to other independentClientprocess，Figure。

![](https://static.vnpy.com/upload/temp/a67e561d-d94d-43f4-9d40-bb929ed6e0e5.png)

&nbsp;

## RPCserver

### Load Module
RPCService module isvnpy/app/rpc_serviceFolder，Which definesRPCEngine object，For a particularvnpyPackaged processRPCserver，Push the server to perform all the events and processes client requests。

By the following2Loading modesRPCModule：
- Graphics mode：log inVN Station，In the upper application interface checkedRpcService，Figure。
  
![](https://static.vnpy.com/upload/temp/62edff53-74d0-4cab-9041-cc209d0b394f.png)

&nbsp;

- Script mode：userun.pystart upVn Trader，When you import an additional module to write the code below：
```
from vnpy.app.rpc_service import RpcServiceApp
from vnpy.gateway.ctp import CtpGateway
main_engine.add_app(RpcServiceApp)
main_engine.add_gateway(CtpGateway)
```

&nbsp;


### Up and running
enterVn Trader，Connect transaction interface，Such asCTP，Then click on the menu bar“Features”->“Rpcservice”，Enter FigureRPCClick Services“start up”To。note：RPCService not only supports the same physical machine multi-process communication，LAN also supports internal communication，When running on the same machine，Without modifying any parameters。

![](https://static.vnpy.com/upload/temp/44b7223c-a232-4002-9e1f-2067f5e7c30a.png)

&nbsp;

## RPCClient

### Load Interface
RPCThe client also provides2Different load patterns：
- Graphics mode：log inVN Station，In checking the underlying interface interfaceRPCservice，Figure。

![](https://static.vnpy.com/upload/temp/659a156c-2bf2-4053-bd91-2c383aff24b2.png)

&nbsp;

- Script mode：userun.pystart upVn Trader，When you import an additional module to write the code below：

```
from vnpy.gateway.rpc import RpcGateway
main_engine.add_gateway(RpcGateway)
```

&nbsp;

### Connection
From the perspective of the client to see，RpcGatewayIs asCTPGeneral Interface，Eliminating the extra step of input information such as account。Because unity in the service side has been completed，You need only connect to the server and。

enterVnTrader，Click on the menu bar”system“->”connectionRPC“，Click the pop-up window in Figure”connection“To。

![](https://static.vnpy.com/upload/temp/988fc191-2762-48cb-b0fb-77384dc543f9.png)

&nbsp;

## Reference Sample
Reference samples locatedexamples/server_clientUnder contents，These include server processes and client processes。

### Server process
Sample offersrun_server.pyfile，Which definesmain_uiwithmain_terminalfunction，Respectively forGUIMode and no interface mode is activated，These two functions may need to be modified in accordance with，Then you can choose to run a certain function。

- GUImode：GUIMode is activated and the above-mentionedrun.pyStart exactly the same，justrun_server.pyAlready loaded by defaultRPCModule，Users only need to modify the interface to load external transactions of。

- No interface mode：Connection configured in advanceCTPAnd other personal information required transaction interface，Figure：
  
![](https://static.vnpy.com/upload/temp/69010fa2-98c4-47ae-b055-d6709d744385.png)

&nbsp;

### The client process
Sample offersrun_client.py，And the above-mentionedrun.pystart upVnTraderExactly the same way，But here already loaded by defaultRpcinterface。

