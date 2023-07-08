import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenu, QSystemTrayIcon, QFileDialog, QTabWidget, QCheckBox, QPushButton
from PyQt6.QtGui import QIcon, QCloseEvent, QAction
from PyQt6.QtCore import QSize, QSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AutoCopier')
        self.resize(QSize(500,400))
        self.tab = QTabWidget()

        # Home Tab
        home_tab = QWidget()
        home_layout = QVBoxLayout(home_tab)
        label = QLabel('Welcome to AutoCopier')
        home_layout.addWidget(label)
        self.tab.addTab(home_tab, 'Home')

        # Preferences Tab
        preferences_tab = QWidget()
        preferences_layout = QVBoxLayout(preferences_tab)

        self.source_button = QPushButton('Select Source')
        self.source_button.clicked.connect(self.select_source)
        preferences_layout.addWidget(self.source_button)

        self.destination_button = QPushButton('Select Destination')
        self.destination_button.clicked.connect(self.select_destination)
        preferences_layout.addWidget(self.destination_button)

        self.autocopy_button = QCheckBox('Autocopy')
        self.autocopy_button.stateChanged.connect(self.change_state_of_autocopy)
        preferences_layout.addWidget(self.autocopy_button)

        self.tab.addTab(preferences_tab, 'Preferences')
        self.setCentralWidget(self.tab)

        # Menu bar
        menu = self.menuBar().addMenu('File')
        preferences = QAction("Preferences", triggered=self.open_preferences)
        menu.addAction(preferences)

    def open_preferences(self):
        self.tab.setCurrentIndex(1)

    def select_source(self):
        source = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        print(f'Selected Source Directory: {source}')
        # Save to settings
        QSettings().setValue('source_directory', source)

    def select_destination(self):
        destination = QFileDialog.getExistingDirectory(self, 'Select Destination Directory')
        print(f'Selected Destination Directory: {destination}')
        # Save to settings
        QSettings().setValue('destination_directory', destination)

    def change_state_of_autocopy(self, state):
        if state == 0:
            print('Autocopy Deactivated')
            QSettings().setValue('autocopy', False)
        else:
            print('Autocopy Activated')
            QSettings().setValue('autocopy', True)

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.setToolTip('AutoCopier')
        menu = QMenu(parent)

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
    # Add preference option	
    preferences = QAction("Preferences", triggered=main_window.open_preferences)	
    menu.addAction(preferences)

    main_window.show()

    tray_icon = SystemTrayIcon(QIcon("assets/img/iOS/icon(@1x).png"), main_window)
    tray_icon.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()