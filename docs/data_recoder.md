#  quotes record 
 quotes module for recording a collection of real-time quotes ：
-  after the connection interface and start recording module quotes ；
-  by local agreement (vt_symbol) add record mission ；
-  background will automatically call market API interface suscribe() function to automatically subscribe quotes ；
-  market information database_manager module save_bar_data() function /save_tick_data() function loaded into the database . 
  
 note ： currently vnpy supported database SQLite/ MySQL/ PostgreSQL/ MongoDB.  its VnTrader the menu bar “ configuration ” enter “ global configuration ” interface to select database ( the default is SQLite),  or in the user directory .vntrader/vt_setting.json configuration inside directly .  if the user MongoDB， the recorded data is directly loaded into the market MongoDB in . 

&nbsp;



##  load startup 
 enter VN Trader rear ， first landing interface ， the connection CTP； then click on the menu bar “ features ”->" quotes record “ rear ， quotes window will pop record ， figure . 
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/data_recoder/datarecoder.png)

 quote status of the startup module for recording True， starts while cycle ， you can add tasks to achieve real-time quotes record . 
```
    def start(self):
        """"""
        self.active = True
        self.thread.start()

    def run(self):
        """"""
        while self.active:
            try:
                task = self.queue.get(timeout=1)
                task_type, data = task

                if task_type == "tick":
                    database_manager.save_tick_data([data])
                elif task_type == "bar":
                    database_manager.save_bar_data([data])

            except Empty:
                continue
```

&nbsp;

##  start a collection 

-  in “ native code ” select the input required to subscribe quotes ， such as rb1905.SHFE；
-  then click back “K line record ” or “Tick recording ” medium manner “ add to ” options ， it will record a specific task to breed data_recorder_setting.json on ， and to show “K line list of records ” or “Tick record list ” in ， figure . 
-  by queue.put() versus queue.get() asynchronous complete collection of market information task . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/data_recoder/start.png)

&nbsp;

 here are the specific principles of ticker ： if there is no historical record of the contract ， users need to add quotes task ， the connection CTP after recording the interface rb1905.SHFE of tick data ， then call add_tick_recording() function performs the following work ：
1)  create tick_recordings dictionary ；
2)  call interface suscribe() functions subscription prices ；
3)  save the tick_recordings dictionary to json on the file ；
4)  push market recorded events . 

```
    def add_tick_recording(self, vt_symbol: str):
        """"""
        if vt_symbol in self.tick_recordings:
            self.write_log(f" already at Tick record list ：{vt_symbol}")
            return

        contract = self.main_engine.get_contract(vt_symbol)
        if not contract:
            self.write_log(f" can not find contract ：{vt_symbol}")
            return

        self.tick_recordings[vt_symbol] = {}
            "symbol": contract.symbol,
            "exchange": contract.exchange.value,
            "gateway_name": contract.gateway_name
        }

        self.subscribe(contract)
        self.save_setting()
        self.put_event()

        self.write_log(f" add to Tick record success ：{vt_symbol}")
```

 below for add_tick_recording() function inside the subroutine call extended ：

###  subscribe quotes 

 transfer main_engine of suscribe() function to subscribe quotes ， fill in the information required for the symbol, exchange, gateway_name
```
    def subscribe(self, contract: ContractData):
        """"""
        req = SubscribeRequest(
            symbol=contract.symbol,
            exchange=contract.exchange
        )
        self.main_engine.subscribe(req, contract.gateway_name)
```

&nbsp;

###  save the subscription information to json file 

-  the main tick_recordings or bar_recordings by save_json() save function to C:\Users\Administrator\\.vntrader within the folder data_recorder_setting.json on . 
-  that json file is used to store the task quotes record ， when the market starts each module ， will call load_setting() function to get tick_recordings with bar_recordings dictionary ， and then began the task of recording . 
```
setting_filename = "data_recorder_setting.json"
    def save_setting(self):
        """"""
        setting = {
            "tick": self.tick_recordings,
            "bar": self.bar_recordings
        }
        save_json(self.setting_filename, setting)

    def load_setting(self):
        """"""
        setting = load_json(self.setting_filename)
        self.tick_recordings = setting.get("tick", {})
        self.bar_recordings = setting.get("bar", {})        
```

&nbsp;

###  push market recorded events 

-  create a list of records quotes tick_symbols with bar_symbols， and cache data dictionary ；
-  create evnte objects ， its type is EVENT_RECORDER_UPDATE,  content is data dictionary ；
-  transfer event_engine of put() push function event event . 

```
    def put_event(self):
        """"""
        tick_symbols = list(self.tick_recordings.keys())
        tick_symbols.sort()

        bar_symbols = list(self.bar_recordings.keys())
        bar_symbols.sort()

        data = {
            "tick": tick_symbols,
            "bar": bar_symbols
        }

        event = Event(
            EVENT_RECORDER_UPDATE,
            data
        )
        self.event_engine.put(event)
```

&nbsp;

###  quotes event registration record 

register_event() functions are registered 2 kind of events ：EVENT_CONTRACT, EVENT_TICK
- EVENT_CONTRACT event ， call is process_contract_event() function :  from tick_recordings with bar_recordings the dictionary acquisition contract breeds require subscription ； then use subscribe() function to subscribe quotes . 
- EVENT_TICK event ， call is process_tick_event() function ： from tick_recordings with bar_recordings the dictionary acquisition contract breeds require subscription ； then use record_tick() with record_bar() function ， the market pushed to record task queue queue waiting to be executed . 

```
    def register_event(self):
        """"""
        self.event_engine.register(EVENT_TICK, self.process_tick_event)
        self.event_engine.register(EVENT_CONTRACT, self.process_contract_event)

    def process_tick_event(self, event: Event):
        """"""
        tick = event.data

        if tick.vt_symbol in self.tick_recordings:
            self.record_tick(tick)

        if tick.vt_symbol in self.bar_recordings:
            bg = self.get_bar_generator(tick.vt_symbol)
            bg.update_tick(tick)

    def process_contract_event(self, event: Event):
        """"""
        contract = event.data
        vt_symbol = contract.vt_symbol

        if (vt_symbol in self.tick_recordings or vt_symbol in self.bar_recordings):
            self.subscribe(contract)

    def record_tick(self, tick: TickData):
        """"""
        task = ("tick", copy(tick))
        self.queue.put(task)

    def record_bar(self, bar: BarData):
        """"""
        task = ("bar", copy(bar))
        self.queue.put(task)

    def get_bar_generator(self, vt_symbol: str):
        """"""
        bg = self.bar_generators.get(vt_symbol, None)

        if not bg:
            bg = BarGenerator(self.record_bar)
            self.bar_generators[vt_symbol] = bg

        return bg
```

&nbsp;

###  quotes task execution record 

 in while loop ， from queue reads the task queue ， transfer save_tick_data() or save_bar_data() function to record data ， and loaded into the database . 
```
    def run(self):
        """"""
        while self.active:
            try:
                task = self.queue.get(timeout=1)
                task_type, data = task

                if task_type == "tick":
                    database_manager.save_tick_data([data])
                elif task_type == "bar":
                    database_manager.save_bar_data([data])

            except Empty:
                continue
```

&nbsp;




##  the removable recording 

 the removable recording operation ： enter the local code requires the removal variety of contract ， such as rb1905.SHFE.  the native code must “Tick record list ”  or “K line list of records ” in .  to remove Tick recording ， just ”Tick recording “ click on the column ” remove “ button . 

 code below shows how it works ：

-  from tick_recordings dictionary removed vt_symbol
-  transfer save_setting() save function json profiles 
-  the latest push tick_recordings dictionary to continue to record prices ， the original contract to remove species no longer record . 
```
    def remove_tick_recording(self, vt_symbol: str):
        """"""
        if vt_symbol not in self.tick_recordings:
            self.write_log(f" out Tick record list ：{vt_symbol}")
            return

        self.tick_recordings.pop(vt_symbol)
        self.save_setting()
        self.put_event()

        self.write_log(f" remove Tick record success ：{vt_symbol}")
```

&nbsp;

##  stop recording 

 stop recording operation ： only need to manually close the window to stop recording module market prices recorded . 

-  record market status changed False,  stop while cycle ；
-  transfer join() turn off the function thread . 

```
    def close(self):
        """"""
        self.active = False

        if self.thread.isAlive():
            self.thread.join()
```