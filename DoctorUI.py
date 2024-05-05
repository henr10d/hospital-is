from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit)

class DoctorInterface(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle('Doctor Dashboard')
        self.setGeometry(400, 400, 1280, 800)
        self.initUI()
        self.user_id = user_id

    def initUI(self):
        layout = QVBoxLayout(self)
        self.patients_list = QTextEdit("Patients' List:\nJohn Doe, Flu\nJane Smith, Cold")
        self.appointments = QTextEdit("Today's Appointments:\nJohn Doe at 10:00 AM\nJane Smith at 11:00 AM")
        layout.addWidget(self.patients_list)
        layout.addWidget(self.appointments)
