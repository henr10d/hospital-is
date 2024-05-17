from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QTabWidget


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
        self.patients_list = QListWidget()
        # rewrite to take from db
        self.patients_list.addItem("John Doe, Flu")
        self.patients_list.addItem("Jane Smith, Cold")
        self.patients_list.itemClicked.connect(self.patientClicked)
        layout.addWidget(self.patients_list)

        self.addPatientButton = QPushButton("Add Patient")
        layout.addWidget(self.addPatientButton)

        widget.setLayout(layout)
        return widget

    def patientClicked(self, item):
        response = QMessageBox.question(self, 'Delete Patient',
                                        f"Do you want to delete {item.text()}?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            print("Delete patient functionality goes here.")
            # Add actual code to delete patient from the database

    def addPatient(self):
        # This function should handle the logic for adding a new patient
        print("Add patient functionality goes here.")

    def createAppointmentsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.appointments_list = QListWidget()
        # rewrite to take from db
        self.appointments_list.addItem("John Doe at 10:00 AM")
        self.appointments_list.addItem("Jane Smith at 11:00 AM")
        self.appointments_list.itemClicked.connect(self.appointmentClicked)  # Connecting click event
        layout.addWidget(self.appointments_list)

        self.addAppointmentButton = QPushButton("Add Appointment")
        self.addAppointmentButton.clicked.connect(self.addAppointment)
        layout.addWidget(self.addAppointmentButton)

        widget.setLayout(layout)
        return widget

    def appointmentClicked(self, item):
        response = QMessageBox.question(self, 'Cancel Appointment',
                                        f"Do you want to cancel the appointment for {item.text()}?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            print("Cancel appointment functionality goes here.")
            # Add actual code to cancel the appointment in the database

    def addAppointment(self):
        # This function should handle the logic for adding a new appointment
        print("Add appointment functionality goes here.")
