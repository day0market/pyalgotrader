from time import sleep
from vnpy.app.script_trader import ScriptEngine


def run(engine: ScriptEngine):
    """
     the main function of the script strategy explained ：
    1.  the only parameter is the script engine ScriptEngine objects ， general inquiries and requests it to complete the operation 
    2.  this function will start to run through a separate thread ， event strategy module is different from other drivers
    3. while cycle maintenance ， please engine.strategy_active state is determined ， for controlled exit 

     for example application scripting strategy ：
    1.  custom baskets entrust execution algorithm 
    2.  hedging strategies between index futures and a basket of stocks 
    3.  domestic and foreign goods 、 cross-exchange digital currency arbitrage 
    4.  combination index custom monitoring, and message notification quote 
    5.  stock market trading strategies scanning picking class （ ryuichi 、 ryuji ）
    6.  and many more ~~~
    """
    vt_symbols = ["IF1912.CFFEX", "rb2001.SHFE"]

    #  subscribe quotes 
    engine.subscribe(vt_symbols)

    #  get contract information 
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        msg = f" contract information ，{contract}"
        engine.write_log(msg)

    #  continuous operation ， use strategy_active to determine whether to exit the program 
    while engine.strategy_active:
        #  polling get quotes 
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f" the latest market , {tick}"
            engine.write_log(msg)

        #  wait 3 seconds into the next round 
        sleep(3)
