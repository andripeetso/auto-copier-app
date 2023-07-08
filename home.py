import os
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QListView, QPushButton
from PyQt6.QtCore import QStringListModel, Qt
from datetime import datetime, timedelta
from shutil import copy2

class HomeTab(QWidget):
    def __init__(self, parent=None):
        super(HomeTab, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)

        # Add current_category attribute
        self.current_category = "Today"

        # Create horizontal layout for labels
        self.labels_layout = QHBoxLayout()

        self.today_label = QLabel("Today")
        self.today_label.mousePressEvent = self.update_file_list_today
        self.labels_layout.addWidget(self.today_label)

        self.yesterday_label = QLabel("Yesterday")
        self.yesterday_label.mousePressEvent = self.update_file_list_yesterday
        self.labels_layout.addWidget(self.yesterday_label)

        self.all_files_label = QLabel("All files")
        self.all_files_label.mousePressEvent = self.update_file_list_all
        self.labels_layout.addWidget(self.all_files_label)

        self.layout.addLayout(self.labels_layout)

        self.file_list_view = QListView()
        self.layout.addWidget(self.file_list_view)

        self.update_file_list(self.current_category)

        # Adding offload drive button
        self.offload_drive_button = QPushButton('Offload Drive')
        self.offload_drive_button.clicked.connect(self.offload_drive)
        self.layout.addWidget(self.offload_drive_button)

    def update_file_list(self, category=None):
        if category is None:
            category = self.current_category  # use the current category if none is provided
        else:
            self.current_category = category  # update the current category
        
        source_directory = self.parent.config.get('source_directory', '')
        if source_directory:
            if category == "All files":
                files = [f for f in os.listdir(source_directory) if not f.startswith('.')]
            else:
                files = []
                for file in os.listdir(source_directory):
                    if file.startswith('.'):
                        continue

                    full_path = os.path.join(source_directory, file)
                    modification_time = datetime.fromtimestamp(os.path.getmtime(full_path))

                    if category == "Yesterday":
                        if modification_time.date() == datetime.now().date() - timedelta(days=1):
                            files.append(file)
                    elif category == "Today":
                        if modification_time.date() == datetime.now().date():
                            files.append(file)

            model = QStringListModel(files)
            self.file_list_view.setModel(model)

    def update_file_list_today(self, event):
        self.update_file_list("Today")

    def update_file_list_yesterday(self, event):
        self.update_file_list("Yesterday")

    def update_file_list_all(self, event):
        self.update_file_list("All files")

    def offload_drive(self):
        source_directory = self.parent.config.get('source_directory', '')
        destination_directory = self.parent.config.get('destination_directory', '')
        if source_directory and destination_directory:
            model=self.file_list_view.model()
            if model is not None:
                for index in range(model.rowCount()):
                    file = model.data(model.index(index), Qt.ItemDataRole.DisplayRole)
                    try:
                        copy2(os.path.join(source_directory, file), destination_directory)
                        print(f'Copied {file}')
                    except Exception as e:
                        print(f'Failed to copy {file} due to {str(e)}')

        else:
            print('Either source directory or destination directory is not set in the preferences.')
