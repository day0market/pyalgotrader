import multiprocessing
from time import sleep
from datetime import datetime, time
from logging import INFO

from vnpy.event import EventEngine
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine

from vnpy.gateway.ctp import CtpGateway
from vnpy.app.cta_strategy import CtaStrategyApp
from vnpy.app.cta_strategy.base import EVENT_CTA_LOG


SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True


ctp_setting = {
    " username ": "",
    " password ": "",
    " brokers code ": "",
    " transaction server ": "",
    " quotes server ": "",
    " product name ": "",
    " authorized coding ": "",
    " product information ": ""
}


def run_child():
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)
    cta_engine = main_engine.add_app(CtaStrategyApp)
    main_engine.write_log(" main engine created successfully ")

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log(" register an event listener log ")

    main_engine.connect(ctp_setting, "CTP")
    main_engine.write_log(" connection CTP interface ")

    sleep(10)

    cta_engine.init_engine()
    main_engine.write_log("CTA strategy initialization is complete ")

    cta_engine.init_all_strategies()
    sleep(60)   # Leave enough time to complete strategy initialization
    main_engine.write_log("CTA all initialization strategy ")

    cta_engine.start_all_strategies()
    main_engine.write_log("CTA policy start all ")

    while True:
        sleep(1)


def run_parent():
    """
    Running in the parent process.
    """
    print(" start up CTA policy guardian parent process ")

    # Chinese futures market trading period (day/night)
    DAY_START = time(8, 45)
    DAY_END = time(15, 30)

    NIGHT_START = time(20, 45)
    NIGHT_END = time(2, 45)

    child_process = None

    while True:
        current_time = datetime.now().time()
        trading = False

        # Check whether in trading period
        if (
            (current_time >= DAY_START and current_time <= DAY_END)
            or (current_time >= NIGHT_START)
            or (current_time <= NIGHT_END)
        ):
            trading = True

        # Start child process in trading period
        if trading and child_process is None:
            print(" promoter process ")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print(" child process started successfully ")

        #  non-record time the child process exits 
        if not trading and child_process is not None:
            print(" close the child process ")
            child_process.terminate()
            child_process.join()
            child_process = None
            print(" child closes successfully ")

        sleep(5)


if __name__ == "__main__":
    run_parent()
