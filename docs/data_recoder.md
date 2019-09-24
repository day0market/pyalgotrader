# Quotes record
Quotes module for recording a collection of real-time quotes：
- After the connection interface and start recording module Quotes；
- By local agreement(vt_symbol)Add record mission；
- Background will automatically call marketAPIInterfacesuscribe()Function to automatically subscribe Quotes；
- Market informationdatabase_managerModulesave_bar_data()function/save_tick_data()Function loaded into the database。
  
note：CurrentlyvnpySupported databaseSQLite/ MySQL/ PostgreSQL/ MongoDB。ItsVnTraderThe menu bar“Configuration”enter“Global Configuration”Interface to select database(The default isSQLite), Or in the user directory.vntrader/vt_setting.jsonConfiguration inside directly。If the userMongoDB，The recorded data is directly loaded into the marketMongoDBin。

&nbsp;



## Load Startup
enterVN TraderRear，First landing Interface，The connectionCTP；Then click on the menu bar“Features”->"Quotes record“Rear，Quotes window will pop record，Figure。
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/data_recoder/datarecoder.png)

Quote status of the startup module for recordingTrue，Startswhilecycle，You can add tasks to achieve real-time quotes record。
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

## Start a collection

- in“Native code”Select the input required to subscribe Quotes，Such asrb1905.SHFE；
- Then click back“KLine record”or“Tickrecording”Medium manner“Add to”Options，It will record a specific task to breeddata_recorder_setting.jsonon，And to show“KLine list of records”or“TickRecord List”in，Figure。
- byqueue.put()versusqueue.get()Asynchronous complete collection of market information task。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/data_recoder/start.png)

&nbsp;

Here are the specific principles of ticker：If there is no historical record of the contract，Users need to add quotes Task，The connectionCTPAfter recording the interfacerb1905.SHFEoftickdata，Then calladd_tick_recording()Function performs the following work：
1) Createtick_recordingsdictionary；
2) Call interfacesuscribe()Functions subscription prices；
3) Save thetick_recordingsDictionary tojsonOn the File；
4) Push market recorded events。

```
    def add_tick_recording(self, vt_symbol: str):
        """"""
        if vt_symbol in self.tick_recordings:
            self.write_log(f"already atTickRecord list：{vt_symbol}")
            return

        contract = self.main_engine.get_contract(vt_symbol)
        if not contract:
            self.write_log(f"Can not find contract：{vt_symbol}")
            return

        self.tick_recordings[vt_symbol] = {}
            "symbol": contract.symbol,
            "exchange": contract.exchange.value,
            "gateway_name": contract.gateway_name
        }

        self.subscribe(contract)
        self.save_setting()
        self.put_event()

        self.write_log(f"Add toTickRecord success：{vt_symbol}")
```

Below foradd_tick_recording()Function inside the subroutine call extended：

### Subscribe Quotes

transfermain_engineofsuscribe()Function to subscribe Quotes，Fill in the information required for thesymbol、exchange、gateway_name
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

### Save the subscription information tojsonfile

- The maintick_recordingsorbar_recordingsbysave_json()Save function toC:\Users\Administrator\\.vntraderWithin the folderdata_recorder_setting.jsonon。
- ThatjsonFile is used to store the task Quotes record，When the market starts each module，Will callload_setting()Function to gettick_recordingswithbar_recordingsdictionary，And then began the task of recording。
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

### Push market recorded events

- Create a list of records Quotestick_symbolswithbar_symbols，And cachedataDictionary；
- createevnteObjects，Its type isEVENT_RECORDER_UPDATE, Content isdatadictionary；
- transferevent_engineofput()Push functioneventevent。

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

### Quotes event registration record

register_event()Functions are registered2Kind of events：EVENT_CONTRACT、EVENT_TICK
- EVENT_CONTRACTevent，Call isprocess_contract_event()function: Fromtick_recordingswithbar_recordingsThe dictionary acquisition contract breeds require subscription；Then usesubscribe()Function to subscribe Quotes。
- EVENT_TICKevent，Call isprocess_tick_event()function：Fromtick_recordingswithbar_recordingsThe dictionary acquisition contract breeds require subscription；Then userecord_tick()withrecord_bar()function，The market pushed to record taskqueueQueue waiting to be executed。

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

### Quotes task execution record

inwhileLoop，FromqueueReads the task queue，transfersave_tick_data()orsave_bar_data()Function to record data，And loaded into the database。
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




## The removable recording

The removable recording operation：Enter the local code requires the removal variety of contract，Such asrb1905.SHFE。The native code must“TickRecord List” or“KLine list of records”in。To removeTickrecording，Just”Tickrecording“Click on the column”Remove“Button。

Code below shows how it works：

- Fromtick_recordingsDictionary removedvt_symbol
- transfersave_setting()Save functionjsonProfiles
- The latest pushtick_recordingsDictionary to continue to record prices，The original contract to remove species no longer record。
```
    def remove_tick_recording(self, vt_symbol: str):
        """"""
        if vt_symbol not in self.tick_recordings:
            self.write_log(f"OutTickRecord list：{vt_symbol}")
            return

        self.tick_recordings.pop(vt_symbol)
        self.save_setting()
        self.put_event()

        self.write_log(f"RemoveTickRecord success：{vt_symbol}")
```

&nbsp;

## Stop recording

Stop recording operation：Only need to manually close the window to stop recording module market prices recorded。

- Record market status changedFalse, stopwhilecycle；
- transferjoin()Turn off the function thread。

```
    def close(self):
        """"""
        self.active = False

        if self.thread.isAlive():
            self.thread.join()
```