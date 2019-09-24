from vnpy.event import Event
from vnpy.rpc import RpcClient
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.object import (
    SubscribeRequest,
    CancelRequest,
    OrderRequest
)
from vnpy.trader.constant import Exchange


class RpcGateway(BaseGateway):
    """
    VN Trader Gateway for RPC service.
    """

    default_setting = {
        " initiative to request address ": "tcp://127.0.0.1:2014",
        " push subscription address ": "tcp://127.0.0.1:4102"
    }

    exchanges = list(Exchange)

    def __init__(self, event_engine):
        """Constructor"""
        super().__init__(event_engine, "RPC")

        self.symbol_gateway_map = {}

        self.client = RpcClient()
        self.client.callback = self.client_callback

    def connect(self, setting: dict):
        """"""
        req_address = setting[" initiative to request address "]
        pub_address = setting[" push subscription address "]

        self.client.subscribe_topic("")
        self.client.start(req_address, pub_address)

        self.write_log(" servers were successfully connected ， start initialization query ")

        self.query_all()

    def subscribe(self, req: SubscribeRequest):
        """"""
        gateway_name = self.symbol_gateway_map.get(req.vt_symbol, "")
        self.client.subscribe(req, gateway_name)

    def send_order(self, req: OrderRequest):
        """"""
        gateway_name = self.symbol_gateway_map.get(req.vt_symbol, "")
        return self.client.send_order(req, gateway_name)

    def cancel_order(self, req: CancelRequest):
        """"""
        gateway_name = self.symbol_gateway_map.get(req.vt_symbol, "")
        self.client.cancel_order(req, gateway_name)

    def query_account(self):
        """"""
        pass

    def query_position(self):
        """"""
        pass

    def query_all(self):
        """"""
        contracts = self.client.get_all_contracts()
        for contract in contracts:
            self.symbol_gateway_map[contract.vt_symbol] = contract.gateway_name
            contract.gateway_name = self.gateway_name
            self.on_contract(contract)
        self.write_log(" contract information inquiry succeed ")

        accounts = self.client.get_all_accounts()
        for account in accounts:
            account.gateway_name = self.gateway_name
            self.on_account(account)
        self.write_log(" financial information query success ")

        positions = self.client.get_all_positions()
        for position in positions:
            position.gateway_name = self.gateway_name
            self.on_position(position)
        self.write_log(" position information query success ")

        orders = self.client.get_all_orders()
        for order in orders:
            order.gateway_name = self.gateway_name
            self.on_order(order)
        self.write_log(" information inquiry commissioned successfully ")

        trades = self.client.get_all_trades()
        for trade in trades:
            trade.gateway_name = self.gateway_name
            self.on_trade(trade)
        self.write_log(" transaction information query success ")

    def close(self):
        """"""
        self.client.stop()
        self.client.join()

    def client_callback(self, topic: str, event: Event):
        """"""
        if event is None:
            print("none event", topic, event)
            return

        data = event.data

        if hasattr(data, "gateway_name"):
            data.gateway_name = self.gateway_name

        self.event_engine.put(event)
