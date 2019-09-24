from typing import Dict, Tuple

from vnpy.api.tora.vntora import TORA_TSTP_D_Buy, TORA_TSTP_D_Sell, TORA_TSTP_EXD_SSE, \
    TORA_TSTP_EXD_SZSE, TORA_TSTP_OPT_LimitPrice, TORA_TSTP_OST_AllTraded, TORA_TSTP_OST_Canceled, \
    TORA_TSTP_OST_NoTradeQueueing, TORA_TSTP_OST_PartTradedQueueing, TORA_TSTP_OST_Unknown, \
    TORA_TSTP_PID_SHBond, TORA_TSTP_PID_SHFund, TORA_TSTP_PID_SHStock, TORA_TSTP_PID_SZBond, \
    TORA_TSTP_PID_SZFund, TORA_TSTP_PID_SZStock, TORA_TSTP_TC_GFD, TORA_TSTP_TC_IOC, TORA_TSTP_VC_AV

from vnpy.trader.constant import Direction, Exchange, OrderType, Product, Status

EXCHANGE_TORA2VT = {
    TORA_TSTP_EXD_SSE: Exchange.SSE,
    TORA_TSTP_EXD_SZSE: Exchange.SZSE,
    # TORA_TSTP_EXD_HK: Exchange.SEHK,
}
EXCHANGE_VT2TORA = {v: k for k, v in EXCHANGE_TORA2VT.items()}

PRODUCT_TORA2VT = {
    #  common ( internal use )
    # TORA_TSTP_PID_COMMON: 0,
    #  shanghai stock 
    TORA_TSTP_PID_SHStock: Product.EQUITY,
    #  shanghai allotment with debt 
    # TORA_TSTP_PID_SHWarrant: 0,
    #  shanghai fund 
    TORA_TSTP_PID_SHFund: Product.FUND,
    #  shanghai bond 
    TORA_TSTP_PID_SHBond: Product.BOND,
    #  shanghai standard ticket 
    # TORA_TSTP_PID_SHStandard: 0,
    #  shanghai pledged repo 
    # TORA_TSTP_PID_SHRepurchase: 0,
    #  shenzhen stock 
    TORA_TSTP_PID_SZStock: Product.EQUITY,
    #  shenzhen allotment with debt 
    # TORA_TSTP_PID_SZWarrant: 0,
    #  shenzhen fund 
    TORA_TSTP_PID_SZFund: Product.FUND,
    #  shenzhen bond 
    TORA_TSTP_PID_SZBond: Product.BOND,
    #  shenzhen standard ticket 
    # TORA_TSTP_PID_SZStandard: 0,
    #  shenzhen pledged repo 
    # TORA_TSTP_PID_SZRepurchase: 0,
}
PRODUCT_VT2TORA = {v: k for k, v in PRODUCT_TORA2VT.items()}

DIRECTION_TORA2VT = {
    #  buy 
    TORA_TSTP_D_Buy: Direction.LONG,
    #  sell 
    TORA_TSTP_D_Sell: Direction.SHORT,
    # # ETF purchase 
    # TORA_TSTP_D_ETFPur: 0,
    # # ETF redemption 
    # TORA_TSTP_D_ETFRed: 0,
    # #  subscription of new shares 
    # TORA_TSTP_D_IPO: 0,
    # #  repo 
    # TORA_TSTP_D_Repurchase: 0,
    # #  reverse repurchase 
    # TORA_TSTP_D_ReverseRepur: 0,
    # #  open-end mutual fund purchase 
    # TORA_TSTP_D_OeFundPur: 0,
    # #  open-end fund redemption 
    # TORA_TSTP_D_OeFundRed: 0,
    # #  collateral included 
    # TORA_TSTP_D_CollateralIn: 0,
    # #  collateral draw 
    # TORA_TSTP_D_CollateralOut: 0,
    # #  pledge storage 
    # TORA_TSTP_D_PledgeIn: 0,
    # #  a library pledge 
    # TORA_TSTP_D_PledgeOut: 0,
    # #  allotment with debt 
    # TORA_TSTP_D_Rationed: 0,
    # #  open-end funds split 
    # TORA_TSTP_D_Split: 0,
    # #  open-end fund merger 
    # TORA_TSTP_D_Merge: 0,
    # #  financing to buy 
    # TORA_TSTP_D_MarginBuy: 0,
    # #  short selling 
    # TORA_TSTP_D_ShortSell: 0,
    # #  repayment sell tickets 
    # TORA_TSTP_D_SellRepayment: 0,
    # #  coupons also buy tickets 
    # TORA_TSTP_D_BuyRepayment: 0,
    # #  coupons also transfer 
    # TORA_TSTP_D_SecurityRepay: 0,
    # #  i transfer vouchers 
    # TORA_TSTP_D_RemainTransfer: 0,
    # #  debt 
    # TORA_TSTP_D_BondConvertStock: 0,
    # #  bond sale back 
    # TORA_TSTP_D_BondPutback: 0,
}
DIRECTION_VT2TORA = {v: k for k, v in DIRECTION_TORA2VT.items()}

# OrderType-> (OrderPriceType, TimeCondition, VolumeCondition)
ORDER_TYPE_VT2TORA: Dict[OrderType, Tuple[str, str, str]] = {
    OrderType.FOK: (TORA_TSTP_OPT_LimitPrice, TORA_TSTP_TC_IOC, TORA_TSTP_VC_AV),
    OrderType.FAK: (TORA_TSTP_OPT_LimitPrice, TORA_TSTP_TC_IOC, TORA_TSTP_VC_AV),
    OrderType.LIMIT: (TORA_TSTP_OPT_LimitPrice, TORA_TSTP_TC_GFD, TORA_TSTP_VC_AV),
}

ORDER_TYPE_TORA2VT: Dict[Tuple[str, str, str], OrderType] = {
    v: k for k, v in ORDER_TYPE_VT2TORA.items()
}

ORDER_STATUS_TORA2VT: Dict[str, Status] = {
    #  all transactions 
    TORA_TSTP_OST_AllTraded: Status.ALLTRADED,
    #  part of the deal is still in the queue 
    TORA_TSTP_OST_PartTradedQueueing: Status.PARTTRADED,
    #  not part of the transaction queue 
    # TORA_TSTP_OST_PartTradedNotQueueing: _,
    #  unsold still in the queue 
    TORA_TSTP_OST_NoTradeQueueing: Status.NOTTRADED,
    #  not in the queue unconcluded 
    # TORA_TSTP_OST_NoTradeNotQueueing: _,
    #  withdrawals 
    TORA_TSTP_OST_Canceled: Status.CANCELLED,
    #  unknown 
    TORA_TSTP_OST_Unknown: Status.NOTTRADED,  # todo: unknown status???
    #  not yet triggered 
    # TORA_TSTP_OST_NotTouched: _,
    #  triggered 
    # TORA_TSTP_OST_Touched: _,
    #  embedded 
    # TORA_TSTP_OST_Cached: _,
}
