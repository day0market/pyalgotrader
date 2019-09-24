from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import QtWidgets
from ..engine import APP_NAME


class RiskManager(QtWidgets.QDialog):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine
        self.rm_engine = main_engine.get_engine(APP_NAME)

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle(" transaction risk control ")

        # Create widgets
        self.active_combo = QtWidgets.QComboBox()
        self.active_combo.addItems([" stop ", " start up "])

        self.flow_limit_spin = RiskManagerSpinBox()
        self.flow_clear_spin = RiskManagerSpinBox()
        self.size_limit_spin = RiskManagerSpinBox()
        self.trade_limit_spin = RiskManagerSpinBox()
        self.active_limit_spin = RiskManagerSpinBox()
        self.cancel_limit_spin = RiskManagerSpinBox()

        save_button = QtWidgets.QPushButton(" storage ")
        save_button.clicked.connect(self.save_setting)

        # Form layout
        form = QtWidgets.QFormLayout()
        form.addRow(" wind control operating status ", self.active_combo)
        form.addRow(" principal flow control limit （ pen ）", self.flow_limit_spin)
        form.addRow(" empty flow control commission （ second ）", self.flow_clear_spin)
        form.addRow(" the upper limit of single commission （ quantity ）", self.size_limit_spin)
        form.addRow(" the total turnover limit （ pen ）", self.trade_limit_spin)
        form.addRow(" limit activity delegates （ pen ）", self.active_limit_spin)
        form.addRow(" contract cancellation limit （ pen ）", self.cancel_limit_spin)
        form.addRow(save_button)

        self.setLayout(form)

        # Set Fix Size
        hint = self.sizeHint()
        self.setFixedSize(hint.width() * 1.2, hint.height())

    def save_setting(self):
        """"""
        active_text = self.active_combo.currentText()
        if active_text == " start up ":
            active = True
        else:
            active = False

        setting = {
            "active": active,
            "order_flow_limit": self.flow_limit_spin.value(),
            "order_flow_clear": self.flow_clear_spin.value(),
            "order_size_limit": self.size_limit_spin.value(),
            "trade_limit": self.trade_limit_spin.value(),
            "active_order_limit": self.active_limit_spin.value(),
            "order_cancel_limit": self.cancel_limit_spin.value(),
        }

        self.rm_engine.update_setting(setting)
        self.rm_engine.save_setting()

        self.close()

    def update_setting(self):
        """"""
        setting = self.rm_engine.get_setting()
        if setting["active"]:
            self.active_combo.setCurrentIndex(1)
        else:
            self.active_combo.setCurrentIndex(0)

        self.flow_limit_spin.setValue(setting["order_flow_limit"])
        self.flow_clear_spin.setValue(setting["order_flow_clear"])
        self.size_limit_spin.setValue(setting["order_size_limit"])
        self.trade_limit_spin.setValue(setting["trade_limit"])
        self.active_limit_spin.setValue(setting["active_order_limit"])
        self.cancel_limit_spin.setValue(setting["order_cancel_limit"])

    def exec_(self):
        """"""
        self.update_setting()
        super().exec_()


class RiskManagerSpinBox(QtWidgets.QSpinBox):
    """"""

    def __init__(self, value: int = 0):
        """"""
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(1000000)
        self.setValue(value)
