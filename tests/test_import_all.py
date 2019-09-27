# flake8: noqa
import unittest
from os import environ


def check_env(key: str, default=None):
    return environ.get(key, default)


def skip_if_module_not_built(env_key: str):
    return unittest.skipIf(
        check_env(key=env_key) == '0',
        f"Skip because of {env_key}==0",
    )


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
class CoreImportTest(unittest.TestCase):

    def test_import_event_engine(self):
        from vnpy.event import EventEngine

    def test_import_main_engine(self):
        from vnpy.trader.engine import MainEngine

    def test_import_ui(self):
        from vnpy.trader.ui import MainWindow, create_qapp


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
class GatewayImportTest(unittest.TestCase):

    def test_import_binance(self):
        from vnpy.gateway.binance import BinanceGateway

    def test_import_bitfinex(self):
        from vnpy.gateway.bitfinex import BitfinexGateway

    def test_import_bitmex(self):
        from vnpy.gateway.bitmex import BitmexGateway

    def test_import_hbdm(self):
        from vnpy.gateway.hbdm import HbdmGateway

    def test_import_huobi(self):
        from vnpy.gateway.huobi import HuobiGateway

    def test_import_ib(self):
        from vnpy.gateway.ib import IbGateway

    def test_import_okex(self):
        from vnpy.gateway.okex import OkexGateway

    def test_import_okexf(self):
        from vnpy.gateway.okexf import OkexfGateway

    def test_import_onetoken(self):
        from vnpy.gateway.onetoken import OnetokenGateway

    def test_import_tiger(self):
        from vnpy.gateway.tiger import TigerGateway


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
class AppImportTest(unittest.TestCase):

    def test_import_cta_strategy_app(self):
        from vnpy.app.cta_strategy import CtaStrategyApp

    def test_import_csv_loader_app(self):
        from vnpy.app.csv_loader import CsvLoaderApp


if __name__ == '__main__':
    unittest.main()
