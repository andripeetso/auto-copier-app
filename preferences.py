from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLineEdit, QCheckBox
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QCoreApplication

class PreferencesTab(QWidget):
    def __init__(self, parent=None):
        super(PreferencesTab, self).__init__(parent)
        self.parent = parent

        self.preferences_layout = QVBoxLayout()

        self.source_button = QPushButton('Select Source')
        self.source_button.clicked.connect(self.select_source)
        self.preferences_layout.addWidget(self.source_button)

        # Source directory input box
        self.source_input = QLineEdit(self.parent.config.get('source_directory', ''))
        self.preferences_layout.addWidget(self.source_input)

        self.destination_button = QPushButton('Select Destination')
        self.destination_button.clicked.connect(self.select_destination)
        self.preferences_layout.addWidget(self.destination_button)

        # Destination directory input box
        self.destination_input = QLineEdit(self.parent.config.get('destination_directory', ''))
        self.preferences_layout.addWidget(self.destination_input)

        self.autocopy_button = QCheckBox('Copy automatically when drive is connected')
        self.autocopy_button.setChecked(self.parent.config.get('autocopy', False))
        self.autocopy_button.stateChanged.connect(self.change_state_of_autocopy)
        self.preferences_layout.addWidget(self.autocopy_button)

        # Set the layout on the widget
        self.setLayout(self.preferences_layout)

    def select_source(self):
        source = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if source:
            print(f'Selected Source Directory: {source}')
            self.source_input.setText(source)
            self.parent.save_to_config('source_directory', source)
            self.parent.update_config()  # Update the main configuration

    def select_destination(self):
        destination = QFileDialog.getExistingDirectory(self, 'Select Destination Directory')
        print(f'Selected Destination Directory: {destination}')
        self.destination_input.setText(destination)
        self.parent.save_to_config('destination_directory', destination)

    def change_state_of_autocopy(self, state):
        if state == 0:
            print('Autocopy Deactivated')
            self.parent.save_to_config('autocopy', False)
        else:
            print('Autocopy Activated')
            self.parent.save_to_config('autocopy', True)
