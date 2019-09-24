# CSVLoad module

CSVLoad modulevnpyThe root directoryvnpy\app\csv_loaderFolder，engine.pyinsideCsvLoaderEngineClass responsible for loading functions to achieve。

## Initial Configuration
Initialization data loading information，It can be divided3class：

- CSVfile path
- Contract Information：Contracts Code、Exchange、KLine cycle
- CSVHeader information：Date Time、Opening price、Highest Price、Lowest、Closing price、Volume

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
WithSQLDatabase as an example：The last issue of theIF1909Historical data into the database，Then the contract should fill in the coderb1909，Fill in exchangeSHFE，There will be a local databasesymbolwithexchangeTwo key values ​​for the index。

&nbsp;

## Loading data

Read from the file pathCSVfile，Then load the data in each iteration to the database。
```
        with open(file_path, "rt") as f:
            reader = csv.DictReader(f)

            for item in reader:
```

&nbsp;

The method of loading data may be divided into2class：
- Directly into：Contracts Code、Exchange、KLine cycle、Volume、Opening price、Highest Price、Lowest、Closing price、Interface name
- Need to be addressed：Date Time（According to their respective time format，bystrptime()Transforming into a time-tuple）、vt_symbol(Contracts Code.Exchange format，Such asrb1909.SHFE)

note：db_bar.replace()For data update，That is replacing the old data into the new。
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

