"""
Implements main window of VN Trader.
"""

from functools import partial
from importlib import import_module
from typing import Callable

from PyQt5 import QtCore, QtGui, QtWidgets

from vnpy.event import EventEngine
from .widget import (
    TickMonitor,
    OrderMonitor,
    TradeMonitor,
    PositionMonitor,
    AccountMonitor,
    LogMonitor,
    ActiveOrderMonitor,
    ConnectDialog,
    ContractManager,
    TradingWidget,
    GlobalDialog
)
from ..engine import MainEngine
from ..utility import get_icon_path, TRADER_DIR


class MainWindow(QtWidgets.QMainWindow):
    """
    Main window of VN Trader.
    """

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super(MainWindow, self).__init__()
        self.main_engine = main_engine
        self.event_engine = event_engine

        self.window_title = f"Algo Trader [{TRADER_DIR}]"

        self.connect_dialogs = {}
        self.widgets = {}

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle(self.window_title)
        self.init_dock()
        self.init_toolbar()
        self.init_menu()
        self.load_window_setting("custom")

    def init_dock(self):
        """"""
        self.trading_widget, trading_dock = self.create_dock(
            TradingWidget, "Manual Trade", QtCore.Qt.LeftDockWidgetArea
        )
        tick_widget, tick_dock = self.create_dock(
            TickMonitor, "Quotes", QtCore.Qt.RightDockWidgetArea
        )
        order_widget, order_dock = self.create_dock(
            OrderMonitor, "Orders", QtCore.Qt.RightDockWidgetArea
        )
        active_widget, active_dock = self.create_dock(
            ActiveOrderMonitor, "Active Orders", QtCore.Qt.RightDockWidgetArea
        )
        trade_widget, trade_dock = self.create_dock(
            TradeMonitor, "Trades", QtCore.Qt.RightDockWidgetArea
        )
        log_widget, log_dock = self.create_dock(
            LogMonitor, "Journal", QtCore.Qt.BottomDockWidgetArea
        )
        account_widget, account_dock = self.create_dock(
            AccountMonitor, "Funds", QtCore.Qt.BottomDockWidgetArea
        )
        position_widget, position_dock = self.create_dock(
            PositionMonitor, "Positions", QtCore.Qt.BottomDockWidgetArea
        )

        self.tabifyDockWidget(active_dock, order_dock)

        self.save_window_setting("default")

    def init_menu(self):
        """"""
        bar = self.menuBar()

        # System menu
        sys_menu = bar.addMenu("Connection")

        gateway_names = self.main_engine.get_all_gateway_names()
        for name in gateway_names:
            func = partial(self.connect, name)
            self.add_menu_action(sys_menu, f"Connection {name}", "connect.ico", func)

        sys_menu.addSeparator()

        self.add_menu_action(sys_menu, "Exit", "exit.ico", self.close)

        # App menu
        app_menu = bar.addMenu("Apps")

        all_apps = self.main_engine.get_all_apps()
        for app in all_apps:
            ui_module = import_module(app.app_module + ".ui")
            widget_class = getattr(ui_module, app.widget_name)

            func = partial(self.open_widget, widget_class, app.app_name)
            icon_path = str(app.app_path.joinpath("ui", app.icon_name))
            self.add_menu_action(
                app_menu, app.display_name, icon_path, func
            )
            self.add_toolbar_action(
                app.display_name, icon_path, func
            )

        # Global setting editor
        action = QtWidgets.QAction("Settings", self)
        action.triggered.connect(self.edit_global_setting)
        bar.addAction(action)

        # Help menu
        help_menu = bar.addMenu("Help")

        self.add_menu_action(
            help_menu,
            "find instrument",
            "contract.ico",
            partial(self.open_widget, ContractManager, "contract"),
        )
        self.add_toolbar_action(
            "find instrument",
            "contract.ico",
            partial(self.open_widget, ContractManager, "contract")
        )

        self.add_menu_action(
            help_menu, " restore window ", "restore.ico", self.restore_window_setting
        )

        self.add_menu_action(
            help_menu, "test email", "email.ico", self.send_test_email
        )

    def init_toolbar(self):
        """"""
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        # Set button size
        w = 40
        size = QtCore.QSize(w, w)
        self.toolbar.setIconSize(size)

        # Set button spacing
        self.toolbar.layout().setSpacing(10)

        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

    def add_menu_action(
            self,
            menu: QtWidgets.QMenu,
            action_name: str,
            icon_name: str,
            func: Callable,
    ):
        """"""
        icon = QtGui.QIcon(get_icon_path(__file__, icon_name))

        action = QtWidgets.QAction(action_name, self)
        action.triggered.connect(func)
        action.setIcon(icon)

        menu.addAction(action)

    def add_toolbar_action(
            self,
            action_name: str,
            icon_name: str,
            func: Callable,
    ):
        """"""
        icon = QtGui.QIcon(get_icon_path(__file__, icon_name))

        action = QtWidgets.QAction(action_name, self)
        action.triggered.connect(func)
        action.setIcon(icon)

        self.toolbar.addAction(action)

    def create_dock(
            self, widget_class: QtWidgets.QWidget, name: str, area: int
    ):
        """
        Initialize a dock widget.
        """
        widget = widget_class(self.main_engine, self.event_engine)

        dock = QtWidgets.QDockWidget(name)
        dock.setWidget(widget)
        dock.setObjectName(name)
        dock.setFeatures(dock.DockWidgetFloatable | dock.DockWidgetMovable)
        self.addDockWidget(area, dock)
        return widget, dock

    def connect(self, gateway_name: str):
        """
        Open connect dialog for gateway connection.
        """
        dialog = self.connect_dialogs.get(gateway_name, None)
        if not dialog:
            dialog = ConnectDialog(self.main_engine, gateway_name)

        dialog.exec_()

    def closeEvent(self, event):
        """
        Call main engine close function before exit.
        """
        reply = QtWidgets.QMessageBox.question(
            self,
            "Exit",
            "Close platform?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )

        if reply == QtWidgets.QMessageBox.Yes:
            for widget in self.widgets.values():
                widget.close()
            self.save_window_setting("custom")

            self.main_engine.close()

            event.accept()
        else:
            event.ignore()

    def open_widget(self, widget_class: QtWidgets.QWidget, name: str):
        """
        Open contract manager.
        """
        widget = self.widgets.get(name, None)
        if not widget:
            widget = widget_class(self.main_engine, self.event_engine)
            self.widgets[name] = widget

        if isinstance(widget, QtWidgets.QDialog):
            widget.exec_()
        else:
            widget.show()

    def save_window_setting(self, name: str):
        """
        Save current window size and state by trader path and setting name.
        """
        settings = QtCore.QSettings(self.window_title, name)
        settings.setValue("state", self.saveState())
        settings.setValue("geometry", self.saveGeometry())

    def load_window_setting(self, name: str):
        """
        Load previous window size and state by trader path and setting name.
        """
        settings = QtCore.QSettings(self.window_title, name)
        state = settings.value("state")
        geometry = settings.value("geometry")

        if isinstance(state, QtCore.QByteArray):
            self.restoreState(state)
            self.restoreGeometry(geometry)

    def restore_window_setting(self):
        """
        Restore window to default setting.
        """
        self.load_window_setting("default")
        self.showMaximized()

    def send_test_email(self):
        """
        Sending a test email.
        """
        self.main_engine.send_email("VN Trader", "testing")

    def edit_global_setting(self):
        """
        """
        dialog = GlobalDialog()
        dialog.exec_()
