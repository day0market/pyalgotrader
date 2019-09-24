"""
General constant string used in VN Trader.
"""

from enum import Enum


class Direction(Enum):
    """
    Direction of order/trade/position.
    """
    LONG = " many "
    SHORT = " air "
    NET = " net "


class Offset(Enum):
    """
    Offset of order/trade.
    """
    NONE = ""
    OPEN = " open "
    CLOSE = " level "
    CLOSETODAY = " flat now "
    CLOSEYESTERDAY = " ping yesterday "


class Status(Enum):
    """
    Order status.
    """
    SUBMITTING = " submitting "
    NOTTRADED = " unsold "
    PARTTRADED = " part of the transaction "
    ALLTRADED = " all transactions "
    CANCELLED = " revoked "
    REJECTED = " single refused "


class Product(Enum):
    """
    Product class.
    """
    EQUITY = " stock "
    FUTURES = " futures "
    OPTION = " options "
    INDEX = " index "
    FOREX = " exchange "
    SPOT = " stock "
    ETF = "ETF"
    BOND = " bond "
    WARRANT = " warrants "
    SPREAD = " spread "
    FUND = " fund "


class OrderType(Enum):
    """
    Order type.
    """
    LIMIT = " limit "
    MARKET = " market price "
    STOP = "STOP"
    FAK = "FAK"
    FOK = "FOK"


class OptionType(Enum):
    """
    Option type.
    """
    CALL = " call option "
    PUT = " put option "


class Exchange(Enum):
    """
    Exchange.
    """
    # Chinese
    CFFEX = "CFFEX"         # China Financial Futures Exchange
    SHFE = "SHFE"           # Shanghai Futures Exchange
    CZCE = "CZCE"           # Zhengzhou Commodity Exchange
    DCE = "DCE"             # Dalian Commodity Exchange
    INE = "INE"             # Shanghai International Energy Exchange
    SSE = "SSE"             # Shanghai Stock Exchange
    SZSE = "SZSE"           # Shenzhen Stock Exchange
    SGE = "SGE"             # Shanghai Gold Exchange
    WXE = "WXE"             # Wuxi Steel Exchange

    # Global
    SMART = "SMART"         # Smart Router for US stocks
    NYMEX = "NYMEX"         # New York Mercantile Exchange
    COMEX = "COMEX"         # a division of theNew York Mercantile Exchange
    GLOBEX = "GLOBEX"       # Globex of CME
    IDEALPRO = "IDEALPRO"   # Forex ECN of Interactive Brokers
    CME = "CME"             # Chicago Mercantile Exchange
    ICE = "ICE"             # Intercontinental Exchange
    SEHK = "SEHK"           # Stock Exchange of Hong Kong
    HKFE = "HKFE"           # Hong Kong Futures Exchange
    SGX = "SGX"             # Singapore Global Exchange
    CBOT = "CBT"            # Chicago Board of Trade
    CBOE = "CBOE"           # Chicago Board Options Exchange
    CFE = "CFE"             # CBOE Futures Exchange
    DME = "DME"             # Dubai Mercantile Exchange
    EUREX = "EUX"           # Eurex Exchange
    APEX = "APEX"           # Asia Pacific Exchange
    LME = "LME"             # London Metal Exchange
    BMD = "BMD"             # Bursa Malaysia Derivatives
    TOCOM = "TOCOM"         # Tokyo Commodity Exchange
    EUNX = "EUNX"           # Euronext Exchange
    KRX = "KRX"             # Korean Exchange

    # CryptoCurrency
    BITMEX = "BITMEX"
    OKEX = "OKEX"
    HUOBI = "HUOBI"
    BITFINEX = "BITFINEX"
    BINANCE = "BINANCE"
    COINBASE = "COINBASE"

    # Special Function
    LOCAL = "LOCAL"         # For local generated data


class Currency(Enum):
    """
    Currency.
    """
    USD = "USD"
    HKD = "HKD"
    CNY = "CNY"


class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    HOUR = "1h"
    DAILY = "d"
    WEEKLY = "w"
