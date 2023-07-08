import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenu, QSystemTrayIcon, QFileDialog, QTabWidget
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QSize
from home import HomeTab
from preferences import PreferencesTab
from shutil import copy2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Read configuration from file
        self.config = self.read_from_config()

        self.setWindowTitle('AutoCopier')
        self.resize(QSize(500,400))
        self.tab = QTabWidget()

        # Home Tab
        self.home_tab = HomeTab(self)
        self.tab.addTab(self.home_tab, 'Home')
        self.home_tab.update_file_list("Today")  # Call update_file_list with "Today"

        # Preferences Tab
        self.preferences_tab = PreferencesTab(self)
        self.tab.addTab(self.preferences_tab, 'Preferences')

        self.setCentralWidget(self.tab)

        # Menu bar
        menu = self.menuBar().addMenu('File')
        preferences = QAction("Preferences", triggered=self.open_preferences)
        menu.addAction(preferences)

    def update_config(self):
        self.config = self.read_from_config()
        self.home_tab.update_file_list()  # use current category

    def open_preferences(self):
        self.tab.setCurrentIndex(1)

    def save_to_config(self, key, value):
        config = {}
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)

        config[key] = value

        with open('config.json', 'w') as f:
            json.dump(config, f)

    def read_from_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        return {}
    
    def offload_drive(self):
        self.home_tab.offload_drive()

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.setToolTip('AutoCopier')
        menu = QMenu(parent)

        offload_drive_action = QAction("Offload Drive")
        offload_drive_action.triggered.connect(self.parent.offload_drive)
        menu.addAction(offload_drive_action)

        open_preferences = QAction("Preferences...")
        open_preferences.triggered.connect(self.on_open_preferences)
        menu.addAction(open_preferences)

        exit_action = QAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)

        self.setContextMenu(menu)

    def on_open_preferences(self):
        self.parent.show()
        self.parent.open_preferences()

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("MyOrganization")
    app.setOrganizationDomain("myorganization.com")
    app.setApplicationName('AutoCopier')
    app.setWindowIcon(QIcon('assets/img/iOS/icon(@2x).png'))

    main_window = MainWindow()

    # Set the menu bar	
    menu = main_window.menuBar().addMenu('File')

    # Add offload drive option
    offload_drive = QAction("Offload Drive", triggered=main_window.offload_drive)
    menu.addAction(offload_drive)

    # Add preference option	
    preferences = QAction("Preferences", triggered=main_window.open_preferences)	
    menu.addAction(preferences)

    main_window.show()

    tray_icon = SystemTrayIcon(QIcon("assets/img/iOS/icon(@1x).png"), main_window)
    tray_icon.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()