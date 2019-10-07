"""
Widget for spread trading.
"""

from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.constant import Direction
from vnpy.trader.ui import QtWidgets, QtCore, QtGui
from vnpy.trader.ui.widget import (
    BaseMonitor, BaseCell,
    BidCell, AskCell,
    TimeCell, PnlCell,
    DirectionCell, EnumCell,
)

from ..engine import (
    SpreadEngine,
    SpreadStrategyEngine,
    APP_NAME,
    EVENT_SPREAD_DATA,
    EVENT_SPREAD_POS,
    EVENT_SPREAD_LOG,
    EVENT_SPREAD_ALGO,
    EVENT_SPREAD_STRATEGY
)


class SpreadManager(QtWidgets.QWidget):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine

        self.spread_engine = main_engine.get_engine(APP_NAME)

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle(" spread trading ")

        self.algo_dialog = SpreadAlgoWidget(self.spread_engine)
        algo_group = self.create_group(" transaction ", self.algo_dialog)
        algo_group.setMaximumWidth(300)

        self.data_monitor = SpreadDataMonitor(
            self.main_engine,
            self.event_engine
        )
        self.log_monitor = SpreadLogMonitor(
            self.main_engine,
            self.event_engine
        )
        self.algo_monitor = SpreadAlgoMonitor(
            self.spread_engine
        )

        self.strategy_monitor = SpreadStrategyMonitor(
            self.spread_engine
        )

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.create_group(" spread ", self.data_monitor), 0, 0)
        grid.addWidget(self.create_group(" journal ", self.log_monitor), 1, 0)
        grid.addWidget(self.create_group(" algorithm ", self.algo_monitor), 0, 1)
        grid.addWidget(self.create_group(" tactics ", self.strategy_monitor), 1, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(algo_group)
        hbox.addLayout(grid)

        self.setLayout(hbox)

    def show(self):
        """"""
        self.spread_engine.start()
        self.algo_dialog.update_class_combo()
        self.showMaximized()

    def create_group(self, title: str, widget: QtWidgets.QWidget):
        """"""
        group = QtWidgets.QGroupBox()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(widget)

        group.setLayout(vbox)
        group.setTitle(title)

        return group


class SpreadDataMonitor(BaseMonitor):
    """
    Monitor for spread data.
    """

    event_type = EVENT_SPREAD_DATA
    data_key = "name"
    sorting = False

    headers = {
        "name": {"display": " name ", "cell": BaseCell, "update": False},
        "bid_volume": {"display": " buy amount ", "cell": BidCell, "update": True},
        "bid_price": {"display": " buying price ", "cell": BidCell, "update": True},
        "ask_price": {"display": " selling price ", "cell": AskCell, "update": True},
        "ask_volume": {"display": " sales volume ", "cell": AskCell, "update": True},
        "net_pos": {"display": " net position ", "cell": PnlCell, "update": True},
        "datetime": {"display": " time ", "cell": TimeCell, "update": True},
        "price_formula": {"display": " pricing ", "cell": BaseCell, "update": False},
        "trading_formula": {"display": " transaction ", "cell": BaseCell, "update": False},
    }

    def register_event(self):
        """
        Register event handler into event engine.
        """
        super().register_event()
        self.event_engine.register(EVENT_SPREAD_POS, self.signal.emit)


class SpreadLogMonitor(QtWidgets.QTextEdit):
    """
    Monitor for log data.
    """
    signal = QtCore.pyqtSignal(Event)

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine

        self.init_ui()
        self.register_event()

    def init_ui(self):
        """"""
        self.setReadOnly(True)

    def register_event(self):
        """"""
        self.signal.connect(self.process_log_event)

        self.event_engine.register(EVENT_SPREAD_LOG, self.signal.emit)

    def process_log_event(self, event: Event):
        """"""
        log = event.data
        msg = f"{log.time.strftime('%H:%M:%S')}\t{log.msg}"
        self.append(msg)


class SpreadAlgoMonitor(BaseMonitor):
    """
    Monitor for algo status.
    """

    event_type = EVENT_SPREAD_ALGO
    data_key = "algoid"
    sorting = False

    headers = {
        "algoid": {"display": " algorithm ", "cell": BaseCell, "update": False},
        "spread_name": {"display": " spread ", "cell": BaseCell, "update": False},
        "direction": {"display": " direction ", "cell": DirectionCell, "update": False},
        "price": {"display": " price ", "cell": BaseCell, "update": False},
        "payup": {"display": " overvalued ", "cell": BaseCell, "update": False},
        "volume": {"display": " quantity ", "cell": BaseCell, "update": False},
        "traded_volume": {"display": " deal ", "cell": BaseCell, "update": True},
        "interval": {"display": " interval ", "cell": BaseCell, "update": False},
        "count": {"display": " count ", "cell": BaseCell, "update": True},
        "status": {"display": " status ", "cell": EnumCell, "update": True},
    }

    def __init__(self, spread_engine: SpreadEngine):
        """"""
        super().__init__(spread_engine.main_engine, spread_engine.event_engine)

        self.spread_engine = spread_engine

    def init_ui(self):
        """
        Connect signal.
        """
        super().init_ui()

        self.setToolTip(" double-click the cell to stop algorithm ")
        self.itemDoubleClicked.connect(self.stop_algo)

    def stop_algo(self, cell):
        """
        Stop algo if cell double clicked.
        """
        algo = cell.get_data()
        self.spread_engine.stop_algo(algo.algoid)


class SpreadAlgoWidget(QtWidgets.QFrame):
    """"""

    def __init__(self, spread_engine: SpreadEngine):
        """"""
        super().__init__()

        self.spread_engine: SpreadEngine = spread_engine
        self.strategy_engine: SpreadStrategyEngine = spread_engine.strategy_engine

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle("Start algo")
        self.setFrameShape(self.Box)
        self.setLineWidth(1)

        self.name_line = QtWidgets.QLineEdit()

        self.direction_combo = QtWidgets.QComboBox()
        self.direction_combo.addItems(
            [Direction.LONG.value, Direction.SHORT.value]
        )

        float_validator = QtGui.QDoubleValidator()

        self.price_line = QtWidgets.QLineEdit()
        self.price_line.setValidator(float_validator)

        self.volume_line = QtWidgets.QLineEdit()
        self.volume_line.setValidator(float_validator)

        int_validator = QtGui.QIntValidator()

        self.payup_line = QtWidgets.QLineEdit()
        self.payup_line.setValidator(int_validator)

        self.interval_line = QtWidgets.QLineEdit()
        self.interval_line.setValidator(int_validator)

        button_start = QtWidgets.QPushButton("Start")
        button_start.clicked.connect(self.start_algo)

        self.lock_combo = QtWidgets.QComboBox()
        self.lock_combo.addItems(
            [" no ", " yes "]
        )

        self.class_combo = QtWidgets.QComboBox()

        add_button = QtWidgets.QPushButton("Add strategy")
        add_button.clicked.connect(self.add_strategy)

        init_button = QtWidgets.QPushButton("Prepare all")
        init_button.clicked.connect(self.strategy_engine.init_all_strategies)

        start_button = QtWidgets.QPushButton("Start all")
        start_button.clicked.connect(self.strategy_engine.start_all_strategies)

        stop_button = QtWidgets.QPushButton("Stop all")
        stop_button.clicked.connect(self.strategy_engine.stop_all_strategies)

        add_spread_button = QtWidgets.QPushButton("Create spread")
        add_spread_button.clicked.connect(self.add_spread)

        remove_spread_button = QtWidgets.QPushButton("Remove spread")
        remove_spread_button.clicked.connect(self.remove_spread)

        form = QtWidgets.QFormLayout()
        form.addRow("spread", self.name_line)
        form.addRow("direction", self.direction_combo)
        form.addRow("price", self.price_line)
        form.addRow("quantity", self.volume_line)
        form.addRow("overvalued", self.payup_line)
        form.addRow("interval", self.interval_line)
        form.addRow("lock", self.lock_combo)
        form.addRow(button_start)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(form)
        vbox.addStretch()
        vbox.addWidget(self.class_combo)
        vbox.addWidget(add_button)
        vbox.addWidget(init_button)
        vbox.addWidget(start_button)
        vbox.addWidget(stop_button)
        vbox.addStretch()
        vbox.addWidget(add_spread_button)
        vbox.addWidget(remove_spread_button)

        self.setLayout(vbox)

    def start_algo(self):
        """"""
        name = self.name_line.text()
        direction = Direction(self.direction_combo.currentText())
        price = float(self.price_line.text())
        volume = float(self.volume_line.text())
        payup = int(self.payup_line.text())
        interval = int(self.interval_line.text())

        lock_str = self.lock_combo.currentText()
        if lock_str == "yes":
            lock = True
        else:
            lock = False

        self.spread_engine.start_algo(
            name, direction, price, volume, payup, interval, lock
        )

    def add_spread(self):
        """"""
        dialog = SpreadDataDialog(self.spread_engine)
        dialog.exec_()

    def remove_spread(self):
        """"""
        dialog = SpreadRemoveDialog(self.spread_engine)
        dialog.exec_()

    def update_class_combo(self):
        """"""
        self.class_combo.addItems(
            self.strategy_engine.get_all_strategy_class_names()
        )

    def remove_strategy(self, strategy_name):
        """"""
        manager = self.managers.pop(strategy_name)
        manager.deleteLater()

    def add_strategy(self):
        """"""
        class_name = str(self.class_combo.currentText())
        if not class_name:
            return

        parameters = self.strategy_engine.get_strategy_class_parameters(
            class_name)
        editor = SettingEditor(parameters, class_name=class_name)
        n = editor.exec_()

        if n == editor.Accepted:
            setting = editor.get_setting()
            spread_name = setting.pop("spread_name")
            strategy_name = setting.pop("strategy_name")

            self.strategy_engine.add_strategy(
                class_name, strategy_name, spread_name, setting
            )


class SpreadDataDialog(QtWidgets.QDialog):
    """"""

    def __init__(self, spread_engine: SpreadEngine):
        """"""
        super().__init__()

        self.spread_engine: SpreadEngine = spread_engine

        self.leg_widgets = []

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle("Create spread")

        self.name_line = QtWidgets.QLineEdit()
        self.active_line = QtWidgets.QLineEdit()

        self.grid = QtWidgets.QGridLayout()

        button_add = QtWidgets.QPushButton("Create spread")
        button_add.clicked.connect(self.add_spread)

        Label = QtWidgets.QLabel

        grid = QtWidgets.QGridLayout()
        grid.addWidget(Label("Spread name"), 0, 0)
        grid.addWidget(self.name_line, 0, 1, 1, 3)
        grid.addWidget(Label("code active leg "), 1, 0)
        grid.addWidget(self.active_line, 1, 1, 1, 3)

        grid.addWidget(Label(""), 2, 0)
        grid.addWidget(Label("native code"), 3, 1)
        grid.addWidget(Label("price multiplier"), 3, 2)
        grid.addWidget(Label("trading multiplier"), 3, 3)

        int_validator = QtGui.QIntValidator()

        leg_count = 5
        for i in range(leg_count):
            symbol_line = QtWidgets.QLineEdit()

            price_line = QtWidgets.QLineEdit()
            price_line.setValidator(int_validator)

            trading_line = QtWidgets.QLineEdit()
            trading_line.setValidator(int_validator)

            grid.addWidget(Label("leg {}".format(i + 1)), 4 + i, 0)
            grid.addWidget(symbol_line, 4 + i, 1)
            grid.addWidget(price_line, 4 + i, 2)
            grid.addWidget(trading_line, 4 + i, 3)

            d = {
                "symbol": symbol_line,
                "price": price_line,
                "trading": trading_line
            }
            self.leg_widgets.append(d)

        grid.addWidget(Label(""), 4 + leg_count, 0,)
        grid.addWidget(button_add, 5 + leg_count, 0, 1, 4)

        self.setLayout(grid)

    def add_spread(self):
        """"""
        spread_name = self.name_line.text()
        if not spread_name:
            QtWidgets.QMessageBox.warning(
                self,
                " creation failed ",
                " please enter the name spread ",
                QtWidgets.QMessageBox.Ok
            )
            return

        active_symbol = self.active_line.text()

        leg_settings = {}
        for d in self.leg_widgets:
            try:
                vt_symbol = d["symbol"].text()
                price_multiplier = int(d["price"].text())
                trading_multiplier = int(d["trading"].text())

                leg_settings[vt_symbol] = {
                    "vt_symbol": vt_symbol,
                    "price_multiplier": price_multiplier,
                    "trading_multiplier": trading_multiplier
                }
            except ValueError:
                pass

        if len(leg_settings) < 2:
            QtWidgets.QMessageBox.warning(
                self,
                " creation failed ",
                " spread requires a minimum of 2 leg ",
                QtWidgets.QMessageBox.Ok
            )
            return

        if active_symbol not in leg_settings:
            QtWidgets.QMessageBox.warning(
                self,
                " creation failed ",
                " each leg is not found in the active leg code ",
                QtWidgets.QMessageBox.Ok
            )
            return

        self.spread_engine.add_spread(
            spread_name,
            list(leg_settings.values()),
            active_symbol
        )
        self.accept()


class SpreadRemoveDialog(QtWidgets.QDialog):
    """"""

    def __init__(self, spread_engine: SpreadEngine):
        """"""
        super().__init__()

        self.spread_engine: SpreadEngine = spread_engine

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle(" spread removed ")
        self.setMinimumWidth(300)

        self.name_combo = QtWidgets.QComboBox()
        spreads = self.spread_engine.get_all_spreads()
        for spread in spreads:
            self.name_combo.addItem(spread.name)

        button_remove = QtWidgets.QPushButton(" remove ")
        button_remove.clicked.connect(self.remove_spread)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.name_combo)
        hbox.addWidget(button_remove)

        self.setLayout(hbox)

    def remove_spread(self):
        """"""
        spread_name = self.name_combo.currentText()
        self.spread_engine.remove_spread(spread_name)
        self.accept()


class SpreadStrategyMonitor(QtWidgets.QWidget):
    """"""

    signal_strategy = QtCore.pyqtSignal(Event)

    def __init__(self, spread_engine: SpreadEngine):
        super().__init__()

        self.strategy_engine = spread_engine.strategy_engine
        self.main_engine = spread_engine.main_engine
        self.event_engine = spread_engine.event_engine

        self.managers = {}

        self.init_ui()
        self.register_event()

    def init_ui(self):
        """"""
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.addStretch()

        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setLayout(self.scroll_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(scroll_area)
        self.setLayout(vbox)

    def register_event(self):
        """"""
        self.signal_strategy.connect(self.process_strategy_event)

        self.event_engine.register(
            EVENT_SPREAD_STRATEGY, self.signal_strategy.emit
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
            manager = SpreadStrategyWidget(self, self.strategy_engine, data)
            self.scroll_layout.insertWidget(0, manager)
            self.managers[strategy_name] = manager

    def remove_strategy(self, strategy_name):
        """"""
        manager = self.managers.pop(strategy_name)
        manager.deleteLater()


class SpreadStrategyWidget(QtWidgets.QFrame):
    """
    Manager for a strategy
    """

    def __init__(
        self,
        strategy_monitor: SpreadStrategyMonitor,
        strategy_engine: SpreadStrategyEngine,
        data: dict
    ):
        """"""
        super().__init__()

        self.strategy_monitor = strategy_monitor
        self.strategy_engine = strategy_engine

        self.strategy_name = data["strategy_name"]
        self._data = data

        self.init_ui()

    def init_ui(self):
        """"""
        self.setFixedHeight(300)
        self.setFrameShape(self.Box)
        self.setLineWidth(1)

        init_button = QtWidgets.QPushButton(" initialization ")
        init_button.clicked.connect(self.init_strategy)

        start_button = QtWidgets.QPushButton(" start up ")
        start_button.clicked.connect(self.start_strategy)

        stop_button = QtWidgets.QPushButton(" stop ")
        stop_button.clicked.connect(self.stop_strategy)

        edit_button = QtWidgets.QPushButton(" edit ")
        edit_button.clicked.connect(self.edit_strategy)

        remove_button = QtWidgets.QPushButton(" remove ")
        remove_button.clicked.connect(self.remove_strategy)

        strategy_name = self._data["strategy_name"]
        spread_name = self._data["spread_name"]
        class_name = self._data["class_name"]
        author = self._data["author"]

        label_text = (
            f"{strategy_name}  -  {spread_name}  ({class_name} by {author})"
        )
        label = QtWidgets.QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.parameters_monitor = StrategyDataMonitor(self._data["parameters"])
        self.variables_monitor = StrategyDataMonitor(self._data["variables"])

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
        self.strategy_engine.init_strategy(self.strategy_name)

    def start_strategy(self):
        """"""
        self.strategy_engine.start_strategy(self.strategy_name)

    def stop_strategy(self):
        """"""
        self.strategy_engine.stop_strategy(self.strategy_name)

    def edit_strategy(self):
        """"""
        strategy_name = self._data["strategy_name"]

        parameters = self.strategy_engine.get_strategy_parameters(
            strategy_name)
        editor = SettingEditor(parameters, strategy_name=strategy_name)
        n = editor.exec_()

        if n == editor.Accepted:
            setting = editor.get_setting()
            self.strategy_engine.edit_strategy(strategy_name, setting)

    def remove_strategy(self):
        """"""
        result = self.strategy_engine.remove_strategy(self.strategy_name)

        # Only remove strategy gui manager if it has been removed from engine
        if result:
            self.strategy_monitor.remove_strategy(self.strategy_name)


class StrategyDataMonitor(QtWidgets.QTableWidget):
    """
    Table monitor for parameters and variables.
    """

    def __init__(self, data: dict):
        """"""
        super().__init__()

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

        # Add spread_name and name edit if add new strategy
        if self.class_name:
            self.setWindowTitle(f"Add strategy ：{self.class_name}")
            button_text = "Add to"
            parameters = {"strategy_name": "", "spread_name": ""}
            parameters.update(self.parameters)
        else:
            self.setWindowTitle(f"New parameters：{self.strategy_name}")
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
