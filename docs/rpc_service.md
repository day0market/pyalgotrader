# RPC service 
 global lock GIL the presence of lead Python only use CPU monocyte count of force .  shown its shortcomings single-process architecture in figure ：

![](https://static.vnpy.com/upload/temp/3f51a477-36db-41d4-9632-75067ba24be7.png)

 use multi-process distributed application architecture can break through the limit .  but the data between each process ， default within the operating system is independently isolated ， can not directly access . 
RPC service just to solve the pain points ：RPC full name Remote-Procedure-Call， chinese “ remote procedure call ”， it is one of the most commonly used cross-process communication .  in vnpy in ， a connected transaction interface acts as a specific process Server character of ， push-event in the local physical machine or internal lan ， pushed to other independent Client process ， figure . 

![](https://static.vnpy.com/upload/temp/a67e561d-d94d-43f4-9d40-bb929ed6e0e5.png)

&nbsp;

## RPC server 

###  load module 
RPC service module is vnpy/app/rpc_service folder ， which defines RPC engine object ， for a particular vnpy packaged process RPC server ， push the server to perform all the events and processes client requests . 

 by the following 2 loading modes RPC module ：
-  graphics mode ： log in VN Station， in the upper application interface checked RpcService， figure . 
  
![](https://static.vnpy.com/upload/temp/62edff53-74d0-4cab-9041-cc209d0b394f.png)

&nbsp;

-  script mode ： use run.py start up Vn Trader， when you import an additional module to write the code below ：
```
from vnpy.app.rpc_service import RpcServiceApp
from vnpy.gateway.ctp import CtpGateway
main_engine.add_app(RpcServiceApp)
main_engine.add_gateway(CtpGateway)
```

&nbsp;


###  up and running 
 enter Vn Trader， connect transaction interface ， such as CTP， then click on the menu bar “ features ”->“Rpc service ”， enter figure RPC click services “ start up ” to .  note ：RPC service not only supports the same physical machine multi-process communication ， lan also supports internal communication ， when running on the same machine ， without modifying any parameters . 

![](https://static.vnpy.com/upload/temp/44b7223c-a232-4002-9e1f-2067f5e7c30a.png)

&nbsp;

## RPC client 

###  load interface 
RPC the client also provides 2 different load patterns ：
-  graphics mode ： log in VN Station， in checking the underlying interface interface RPC service ， figure . 

![](https://static.vnpy.com/upload/temp/659a156c-2bf2-4053-bd91-2c383aff24b2.png)

&nbsp;

-  script mode ： use run.py start up Vn Trader， when you import an additional module to write the code below ：

```
from vnpy.gateway.rpc import RpcGateway
main_engine.add_gateway(RpcGateway)
```

&nbsp;

###  connection 
 from the perspective of the client to see ，RpcGateway is as CTP general interface ， eliminating the extra step of input information such as account .  because unity in the service side has been completed ， you need only connect to the server and . 

 enter VnTrader， click on the menu bar ” system “->” connection RPC“， click the pop-up window in figure ” connection “ to . 

![](https://static.vnpy.com/upload/temp/988fc191-2762-48cb-b0fb-77384dc543f9.png)

&nbsp;

##  reference sample 
 reference samples located examples/server_client under contents ， these include server processes and client processes . 

###  server process 
 sample offers run_server.py file ， which defines main_ui with main_terminal function ， respectively for GUI mode and no interface mode is activated ， these two functions may need to be modified in accordance with ， then you can choose to run a certain function . 

- GUI mode ：GUI mode is activated and the above-mentioned run.py start exactly the same ， just run_server.py already loaded by default RPC module ， users only need to modify the interface to load external transactions of . 

-  no interface mode ： connection configured in advance CTP and other personal information required transaction interface ， figure ：
  
![](https://static.vnpy.com/upload/temp/69010fa2-98c4-47ae-b055-d6709d744385.png)

&nbsp;

###  the client process 
 sample offers run_client.py， and the above-mentioned run.py start up VnTrader exactly the same way ， but here already loaded by default Rpc interface . 

