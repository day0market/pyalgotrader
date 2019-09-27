# CSV load module 

CSV load module vnpy the root directory vnpy\app\csv_loader folder ，engine.py inside CsvLoaderEngine class responsible for loading functions to achieve . 

##  initial configuration 
 initialization data loading information ， it can be divided 3 class ：

- CSV file path 
-  contract information ： contracts code ,  exchange , K line cycle 
- CSV header information ： date time ,  opening price ,  highest price ,  lowest ,  closing price ,  volume 

```
        self.file_path: str = ""

        self.symbol: str = ""
        self.exchange: Exchange = Exchange.SSE
        self.interval: Interval = Interval.MINUTE

        self.datetime_head: str = ""
        self.open_head: str = ""
        self.close_head: str = ""
        self.low_head: str = ""
        self.high_head: str = ""
        self.volume_head: str = ""
```
 with SQL database as an example ： the last issue of the IF1909 historical data into the database ， then the contract should fill in the code rb1909， fill in exchange SHFE， there will be a local database symbol with exchange two key values ​​for the index . 

&nbsp;

##  loading data 

 read from the file path CSV file ， then load the data in each iteration to the database . 
```
        with open(file_path, "rt") as f:
            reader = csv.DictReader(f)

            for item in reader:
```

&nbsp;

 the method of loading data may be divided into 2 class ：
-  directly into ： contracts code ,  exchange , K line cycle ,  volume ,  opening price ,  highest price ,  lowest ,  closing price ,  interface name 
-  need to be addressed ： date time （ according to their respective time format ， by strptime() transforming into a time-tuple ）, vt_symbol( contracts code . exchange format ， such as rb1909.SHFE)

 note ：db_bar.replace() for data update ， that is replacing the old data into the new . 
```
                db_bar.symbol = symbol
                db_bar.exchange = exchange.value
                db_bar.datetime = datetime.strptime(
                    item[datetime_head], datetime_format
                )
                db_bar.interval = interval.value
                db_bar.volume = item[volume_head]
                db_bar.open_price = item[open_head]
                db_bar.high_price = item[high_head]
                db_bar.low_price = item[low_head]
                db_bar.close_price = item[close_head]
                db_bar.vt_symbol = vt_symbol
                db_bar.gateway_name = "DB"

                db_bar.replace()
```

