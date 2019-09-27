"""
Defines constants and objects used in CtaStrategy App.
"""

from dataclasses import dataclass, field
from enum import Enum

from vnpy.trader.constant import Direction, Offset

APP_NAME = "CtaStrategy"
STOPORDER_PREFIX = "STOP"


class StopOrderStatus(Enum):
    WAITING = " waiting "
    CANCELLED = " revoked "
    TRIGGERED = " triggered "


class EngineType(Enum):
    LIVE = " firm "
    BACKTESTING = " backtesting "


class BacktestingMode(Enum):
    BAR = 1
    TICK = 2


@dataclass
class StopOrder:
    vt_symbol: str
    direction: Direction
    offset: Offset
    price: float
    volume: float
    stop_orderid: str
    strategy_name: str
    lock: bool = False
    vt_orderids: list = field(default_factory=list)
    status: StopOrderStatus = StopOrderStatus.WAITING

    def __str__(self):
        return f'[Stop Order {self.stop_orderid}] {self.vt_symbol} ' \
               f'{self.direction} {self.price} {self.volume} [{self.status}]'


EVENT_CTA_LOG = "eCtaLog"
EVENT_CTA_STRATEGY = "eCtaStrategy"
EVENT_CTA_STOPORDER = "eCtaStopOrder"
