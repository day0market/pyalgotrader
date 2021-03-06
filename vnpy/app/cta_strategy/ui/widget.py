from vnpy.event import Event, EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import QtCore, QtGui, QtWidgets
from vnpy.trader.ui.widget import (
    BaseCell,
    EnumCell,
    MsgCell,
    TimeCell,
    BaseMonitor
)
from ..base import (
    APP_NAME,
    EVENT_CTA_LOG,
    EVENT_CTA_STOPORDER,
    EVENT_CTA_STRATEGY
)
from ..engine import CtaEngine


class CtaManager(QtWidgets.QWidget):
    """"""

    signal_log = QtCore.pyqtSignal(Event)
    signal_strategy = QtCore.pyqtSignal(Event)

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super(CtaManager, self).__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine
        self.cta_engine = main_engine.get_engine(APP_NAME)

        self.managers = {}

        self.init_ui()
        self.register_event()
        self.cta_engine.init_engine()
        self.update_class_combo()

    def init_ui(self):
        """"""
        self.setWindowTitle("CTA live trading")

        # Create widgets
        self.class_combo = QtWidgets.QComboBox()

        add_button = QtWidgets.QPushButton("Add strategy")
        add_button.clicked.connect(self.add_strategy)

        init_button = QtWidgets.QPushButton("Prepare All")
        init_button.clicked.connect(self.cta_engine.init_all_strategies)

        start_button = QtWidgets.QPushButton("Start All")
        start_button.clicked.connect(self.cta_engine.start_all_strategies)

        stop_button = QtWidgets.QPushButton("Stop All")
        stop_button.clicked.connect(self.cta_engine.stop_all_strategies)

        clear_button = QtWidgets.QPushButton("Clear log")
        clear_button.clicked.connect(self.clear_log)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.addStretch()

        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setLayout(self.scroll_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        self.log_monitor = LogMonitor(self.main_engine, self.event_engine)

        self.stop_order_monitor = StopOrderMonitor(
            self.main_engine, self.event_engine
        )

        # Set layout
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.class_combo)
        hbox1.addWidget(add_button)
        hbox1.addStretch()
        hbox1.addWidget(init_button)
        hbox1.addWidget(start_button)
        hbox1.addWidget(stop_button)
        hbox1.addWidget(clear_button)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll_area, 0, 0, 2, 1)
        grid.addWidget(self.stop_order_monitor, 0, 1)
        grid.addWidget(self.log_monitor, 1, 1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(grid)

        self.setLayout(vbox)

    def update_class_combo(self):
        """"""
        self.class_combo.addItems(
            self.cta_engine.get_all_strategy_class_names()
        )

    def register_event(self):
        """"""
        self.signal_strategy.connect(self.process_strategy_event)

        self.event_engine.register(
            EVENT_CTA_STRATEGY, self.signal_strategy.emit
        )

    def process_strategy_event(self, event):
        """
        Update strategy status onto its monitor.
        """
        data = event.data
        strategy_name = data["strategy_name"]

        if strategy_name in self.managers:
            manager = self.managers[strategy_name]
            manager.update_data(data)
        else:
            manager = StrategyManager(self, self.cta_engine, data)
            self.scroll_layout.insertWidget(0, manager)
            self.managers[strategy_name] = manager

    def remove_strategy(self, strategy_name):
        """"""
        manager = self.managers.pop(strategy_name)
        manager.deleteLater()

    def add_strategy(self):
        """"""
        class_name = str(self.class_combo.currentText())
        if not class_name:
            return

        parameters = self.cta_engine.get_strategy_class_parameters(class_name)
        editor = SettingEditor(parameters, class_name=class_name)
        n = editor.exec_()

        if n == editor.Accepted:
            setting = editor.get_setting()
            vt_symbol = setting.pop("vt_symbol")
            strategy_name = setting.pop("strategy_name")

            self.cta_engine.add_strategy(
                class_name, strategy_name, vt_symbol, setting
            )

    def clear_log(self):
        """"""
        self.log_monitor.setRowCount(0)

    def show(self):
        """"""
        self.showMaximized()


class StrategyManager(QtWidgets.QFrame):
    """
    Manager for a strategy
    """

    def __init__(
            self, cta_manager: CtaManager, cta_engine: CtaEngine, data: dict
    ):
        """"""
        super(StrategyManager, self).__init__()

        self.cta_manager = cta_manager
        self.cta_engine = cta_engine

        self.strategy_name = data["strategy_name"]
        self._data = data

        self.init_ui()

    def init_ui(self):
        """"""
        self.setFixedHeight(300)
        self.setFrameShape(self.Box)
        self.setLineWidth(1)

        init_button = QtWidgets.QPushButton("Prepare")
        init_button.clicked.connect(self.init_strategy)

        start_button = QtWidgets.QPushButton("Start")
        start_button.clicked.connect(self.start_strategy)

        stop_button = QtWidgets.QPushButton("Stop")
        stop_button.clicked.connect(self.stop_strategy)

        edit_button = QtWidgets.QPushButton("Edit")
        edit_button.clicked.connect(self.edit_strategy)

        remove_button = QtWidgets.QPushButton("Remove")
        remove_button.clicked.connect(self.remove_strategy)

        strategy_name = self._data["strategy_name"]
        vt_symbol = self._data["vt_symbol"]
        class_name = self._data["class_name"]
        author = self._data["author"]

        label_text = (
            f"{strategy_name}  -  {vt_symbol}  ({class_name} by {author})"
        )
        label = QtWidgets.QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.parameters_monitor = DataMonitor(self._data["parameters"])
        self.variables_monitor = DataMonitor(self._data["variables"])

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(init_button)
        hbox.addWidget(start_button)
        hbox.addWidget(stop_button)
        hbox.addWidget(edit_button)
        hbox.addWidget(remove_button)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.parameters_monitor)
        vbox.addWidget(self.variables_monitor)
        self.setLayout(vbox)

    def update_data(self, data: dict):
        """"""
        self._data = data

        self.parameters_monitor.update_data(data["parameters"])
        self.variables_monitor.update_data(data["variables"])

    def init_strategy(self):
        """"""
        self.cta_engine.init_strategy(self.strategy_name)

    def start_strategy(self):
        """"""
        self.cta_engine.start_strategy(self.strategy_name)

    def stop_strategy(self):
        """"""
        self.cta_engine.stop_strategy(self.strategy_name)

    def edit_strategy(self):
        """"""
        strategy_name = self._data["strategy_name"]

        parameters = self.cta_engine.get_strategy_parameters(strategy_name)
        editor = SettingEditor(parameters, strategy_name=strategy_name)
        n = editor.exec_()

        if n == editor.Accepted:
            setting = editor.get_setting()
            self.cta_engine.edit_strategy(strategy_name, setting)

    def remove_strategy(self):
        """"""
        result = self.cta_engine.remove_strategy(self.strategy_name)

        # Only remove strategy gui manager if it has been removed from engine
        if result:
            self.cta_manager.remove_strategy(self.strategy_name)


class DataMonitor(QtWidgets.QTableWidget):
    """
    Table monitor for parameters and variables.
    """

    def __init__(self, data: dict):
        """"""
        super(DataMonitor, self).__init__()

        self._data = data
        self.cells = {}

        self.init_ui()

    def init_ui(self):
        """"""
        labels = list(self._data.keys())
        self.setColumnCount(len(labels))
        self.setHorizontalHeaderLabels(labels)

        self.setRowCount(1)
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(self.NoEditTriggers)

        for column, name in enumerate(self._data.keys()):
            value = self._data[name]

            cell = QtWidgets.QTableWidgetItem(str(value))
            cell.setTextAlignment(QtCore.Qt.AlignCenter)

            self.setItem(0, column, cell)
            self.cells[name] = cell

    def update_data(self, data: dict):
        """"""
        for name, value in data.items():
            cell = self.cells[name]
            cell.setText(str(value))


class StopOrderMonitor(BaseMonitor):
    """
    Monitor for local stop order.
    """

    event_type = EVENT_CTA_STOPORDER
    data_key = "stop_orderid"
    sorting = True

    headers = {
        "stop_orderid": {
            "display": " stop no. commission ",
            "cell": BaseCell,
            "update": False,
        },
        "vt_orderids": {"display": " limit order no. ", "cell": BaseCell, "update": True},
        "vt_symbol": {"display": " native code ", "cell": BaseCell, "update": False},
        "direction": {"display": " direction ", "cell": EnumCell, "update": False},
        "offset": {"display": " offset ", "cell": EnumCell, "update": False},
        "price": {"display": " price ", "cell": BaseCell, "update": False},
        "volume": {"display": " quantity ", "cell": BaseCell, "update": False},
        "status": {"display": " status ", "cell": EnumCell, "update": True},
        "lock": {"display": " lock ", "cell": BaseCell, "update": False},
        "strategy_name": {"display": " strategy name ", "cell": BaseCell, "update": False},
    }


class LogMonitor(BaseMonitor):
    """
    Monitor for log data.
    """

    event_type = EVENT_CTA_LOG
    data_key = ""
    sorting = False

    headers = {
        "time": {"display": " time ", "cell": TimeCell, "update": False},
        "msg": {"display": " information ", "cell": MsgCell, "update": False},
    }

    def init_ui(self):
        """
        Stretch last column.
        """
        super(LogMonitor, self).init_ui()

        self.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch
        )

    def insert_new_row(self, data):
        """
        Insert a new row at the top of table.
        """
        super(LogMonitor, self).insert_new_row(data)
        self.resizeRowToContents(0)


class SettingEditor(QtWidgets.QDialog):
    """
    For creating new strategy and editing strategy parameters.
    """

    def __init__(
            self, parameters: dict, strategy_name: str = "", class_name: str = ""
    ):
        """"""
        super(SettingEditor, self).__init__()

        self.parameters = parameters
        self.strategy_name = strategy_name
        self.class_name = class_name

        self.edits = {}

        self.init_ui()

    def init_ui(self):
        """"""
        form = QtWidgets.QFormLayout()

        # Add vt_symbol and name edit if add new strategy
        if self.class_name:
            self.setWindowTitle(f"Add strategy ：{self.class_name}")
            button_text = "Add to"
            parameters = {"strategy_name": "", "vt_symbol": ""}
            parameters.update(self.parameters)
        else:
            self.setWindowTitle(f"Edit parameters：{self.strategy_name}")
            button_text = "Save"
            parameters = self.parameters

        for name, value in parameters.items():
            type_ = type(value)

            edit = QtWidgets.QLineEdit(str(value))
            if type_ is int:
                validator = QtGui.QIntValidator()
                edit.setValidator(validator)
            elif type_ is float:
                validator = QtGui.QDoubleValidator()
                edit.setValidator(validator)

            form.addRow(f"{name} {type_}", edit)

            self.edits[name] = (edit, type_)

        button = QtWidgets.QPushButton(button_text)
        button.clicked.connect(self.accept)
        form.addRow(button)

        self.setLayout(form)

    def get_setting(self):
        """"""
        setting = {}

        if self.class_name:
            setting["class_name"] = self.class_name

        for name, tp in self.edits.items():
            edit, type_ = tp
            value_text = edit.text()

            if type_ == bool:
                if value_text == "True":
                    value = True
                else:
                    value = False
            else:
                value = type_(value_text)

            setting[name] = value

        return setting
