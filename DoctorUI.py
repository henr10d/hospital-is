from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QTabWidget, QFormLayout, \
    QLineEdit, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy


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
        self.tabWidget.addTab(self.createPersonalInfoPage(), "Personal Info")


        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)

    def createPersonalInfoPage(self):
        widget = QWidget()
        formLayout = QFormLayout()

        self.name_edit = QLineEdit()
        self.age_edit = QLineEdit()

        self.update_name_btn = QPushButton('Update personal info')
        self.load_picture_btn = QPushButton('Add/Change Picture')

        # Creating a horizontal layout to center buttons
        update_btn_layout = QHBoxLayout()
        update_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        update_btn_layout.addWidget(self.update_name_btn)
        update_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        picture_btn_layout = QHBoxLayout()
        picture_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        picture_btn_layout.addWidget(self.load_picture_btn)
        picture_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # chybi db snimky
        # current_picture_path = self.database.fetch_picture(self.user_id)
        # if current_picture_path:
        #     pixmap = QPixmap(current_picture_path)
        #     self.picture_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

        formLayout.addRow("Name:", self.name_edit)
        formLayout.addRow("Age:", self.age_edit)
        formLayout.addRow(update_btn_layout)
        # formLayout.addRow(self.picture_label)
        formLayout.addRow(picture_btn_layout)

        widget.setLayout(formLayout)
        return widget

    # dodelat
    def update_personal_info(self):
        pass

    # dodelat image picker
    def add_picture(self):
        pass

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
            # db

    # patent picker
    def addPatient(self):
        print("Add patient functionality goes here.")


    def createAppointmentsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.appointments_list = QListWidget()
        # rewrite to take from db name, time, date
        self.appointments_list.addItem("John Doe at 10:00 AM")
        self.appointments_list.addItem("Jane Smith at 11:00 AM")
        self.appointments_list.itemClicked.connect(self.appointmentClicked)  # Connecting click event hehe
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

    def addAppointment(self):
        print("Add appointment functionality goes here.")
