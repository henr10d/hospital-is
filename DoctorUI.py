from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QTabWidget)

class DoctorInterface(QWidget):
    def __init__(self, user_id, database):
        self.user_id = user_id
        self.database = database
        super().__init__()
        self.setWindowTitle('Doctor Dashboard')
        self.setGeometry(400, 400, 1280, 800)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
            }
            QLineEdit, QTextEdit {
                border: 2px solid #AAAAAA;
                border-radius: 10px;
                padding: 10px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QPushButton {
                border: 2px solid #0057D8;
                border-radius: 10px;
                padding: 10px;
                background-color: #0057D8;
                color: #FFFFFF;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #007BFF;
                border-color: #007BFF;
            }
            QPushButton:pressed {
                background-color: #0056B3;
                border-color: #004D99;
            }
            QLabel {
                padding: 10px;
                color: #333333;
            }
        """)

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.createPatientsPage(), "Patients")
        self.tabWidget.addTab(self.createAppointmentsPage(), "Appointments")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)

    def createPatientsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.patients_list = QTextEdit()
        self.patients_list.setReadOnly(True)
        self.patients_list.setText("Patients' List:\nJohn Doe, Flu\nJane Smith, Cold")
        layout.addWidget(self.patients_list)
        widget.setLayout(layout)
        return widget

    def createAppointmentsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.appointments = QTextEdit()
        self.appointments.setReadOnly(True)
        self.appointments.setText("Today's Appointments:\nJohn Doe at 10:00 AM\nJane Smith at 11:00 AM")
        layout.addWidget(self.appointments)
        widget.setLayout(layout)
        return widget
