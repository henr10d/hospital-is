import mysql
# from PyQt5 import Qt
from PyQt5.QtCore import Qt
from hashlib import sha256

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QTabWidget, QFormLayout, \
    QLineEdit, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidgetItem, QDialog, QDialogButtonBox


class DoctorInterface(QWidget):
    def __init__(self, doctor, database, username, hospital):
        self.doctor_id = doctor[0]
        self.doctor_name = doctor[2]
        self.doctor_birth = doctor[3]
        self.insurance = doctor[4]
        self.database = database
        self.username = username
        self.hospital = hospital
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
        self.tabWidget.addTab(self.createAcceptedPatientsPage(), "Accepted patients")

        layout = QVBoxLayout(self)
        self.leave_button = QPushButton('To login', self)
        self.leave_button.clicked.connect(self.leave)
        layout.addWidget(self.tabWidget)
        layout.addWidget(self.leave_button)

    def leave(self):
        self.hospital.show()
        self.close()

    def loadAppointments(self):
        self.appointment_list.clear()  # Clear existing items before loading new ones
        # self.database2 = Database()

        # doctor_id = self.database2.get_doctor_id_by_user_id(self.user_id)
        # if not doctor_id:
        #     QMessageBox.critical(self, 'Database Error', 'Failed to find associated doctor ID.')
        #     return

        # appointments = self.database2.fetch_appointments_for_doctor(doctor_id)

        appointments = self.database.fetch_doctor_appointments(self.doctor_id)
        if appointments is None:
            QMessageBox.critical(self, 'Database Error', 'Failed to fetch appointments.')
            return

        for appointment_id, appointment_time, appointment_details, status in appointments:
            if status == "approved":
                color = "\U0001F7E2"  # Green
            elif status == "declined":
                color = "\U0001F534"  # Red
            else:
                color = "\U0001F7E1"  # Yellow
            item_text = f"{color} Time: {appointment_time} - Appointment: {appointment_details}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (appointment_id, status))  # Store appointment ID and current status
            self.appointment_list.addItem(item)

    def createAppointmentsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.appointment_list = QListWidget()
        self.appointment_list.itemClicked.connect(self.appointmentClicked)  # Connect the signal to a method
        layout.addWidget(self.appointment_list)

        self.loadAppointments()  # Load the appointments into the list

        legend_label = QLabel("🟢 Approved \U0001F7E1 Waiting 🔴 Declined")
        layout.addWidget(legend_label)

        return widget

    def addMedicine(self, item):
        patient_id, name = item.data(Qt.UserRole)

        details_dialog = QDialog(self)
        details_dialog.setWindowTitle('Prescribe Medicine')
        layout = QVBoxLayout(details_dialog)

        label = QLabel(f"Medicine to be prescribed for patient: {name}")
        layout.addWidget(label)

        med_name = QLineEdit(details_dialog)
        med_name.setPlaceholderText("Enter the name of the medicine")
        layout.addWidget(med_name)

        med_desc = QLineEdit(details_dialog)
        med_desc.setPlaceholderText("Describe the usage of the medicine")
        layout.addWidget(med_desc)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        button_box.accepted.connect(details_dialog.accept)
        button_box.rejected.connect(details_dialog.reject)
        layout.addWidget(button_box)

        # Ensure the medicine is inserted and dialog is closed when Apply is clicked
        button_box.button(QDialogButtonBox.Ok).clicked.connect(lambda: self.insert_medicine(item, med_name, med_desc))

        details_dialog.setLayout(layout)
        details_dialog.exec_()

    def insert_medicine(self, item, med_name, med_desc):
        patient_id, name = item.data(Qt.UserRole)
        medicine = med_name.text()
        description = med_desc.text()
        self.database.prescribe_medicine(patient_id, self.doctor_id, medicine, description)
        QMessageBox.information(self, 'Medicine prescribed',
                                f'You have successfully prescribed {medicine} for patient {name}')

    def createAcceptedPatientsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.acceptedPatientsList = QListWidget()
        self.acceptedPatientsList.itemClicked.connect(self.addMedicine)  # Connect the signal to a method
        self.loadAcceptedPatients()
        layout.addWidget(self.acceptedPatientsList)

        widget.setLayout(layout)
        return widget

    def loadAcceptedPatients(self):
        self.acceptedPatientsList.clear()
        patients = self.database.fetch_accepted_patients(self.doctor_id)
        if patients is None:
            QMessageBox.critical(self, 'Database Error', 'Failed to fetch appointments.')
            return

        for patient_id, name, birth, insurance in patients:
            date = birth.strftime("%Y-%m-%d")
            item_text = f"{name} Born: {date}, Insurance company: {insurance}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (patient_id, name))  # Store appointment ID and current status
            self.acceptedPatientsList.addItem(item)

    def appointmentClicked(self, item):
        appointment_id, current_status = item.data(Qt.UserRole)
        new_status = 'approved' if current_status != 'approved' else 'declined'
        response = QMessageBox.question(self, 'Change Appointment Status',
                                        f"Do you want to change the appointment status to {'Approved' if new_status == 'approved' else 'Declined'}?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            self.database.update_appointment_status((new_status, appointment_id))
            QMessageBox.information(self, 'Status Updated',
                                    f'Appointment status has been changed to {"Approved" if new_status == "approved" else "Declined"}.')
            # Refresh the list or update the item directly here to show new status
        self.loadAppointments()

    def createPersonalInfoPage(self):
        widget = QWidget()
        layout = QFormLayout()

        nameLabel = QLabel(self.doctor_name if self.doctor_name is not None else '')
        ageLabel = QLabel(self.doctor_birth.strftime("%Y-%m-%d") if self.doctor_birth is not None else '')
        self.username_edit = QLineEdit(self.username if self.username is not None else '')
        self.password_edit = QLineEdit('')

        self.update_name_btn = QPushButton('Update personal info')
        self.update_name_btn.clicked.connect(self.update_personal_info)
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

        layout.addRow("Name:", nameLabel)
        layout.addRow("Age:", ageLabel)
        layout.addRow("Username:", self.username_edit)
        layout.addRow("New password:", self.password_edit)
        layout.addRow(update_btn_layout)
        layout.addRow(update_btn_layout)
        # formLayout.addRow(self.picture_label)
        layout.addRow(picture_btn_layout)

        widget.setLayout(layout)
        return widget

    # dodelat
    def update_personal_info(self):
        new_username = self.username_edit.text()
        new_password = self.password_edit.text()
        if new_username is None or new_username == '' or new_password is None or new_password == '':
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid non empty username and password.')
            return
        self.username = new_username
        password = sha256(new_password.encode()).hexdigest()

        try:
            self.database.update_login_credentials((self.username, password, self.doctor_id))
            QMessageBox.information(self, 'Update Successful',
                                    'Your personal information has been updated successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Update Failed', 'Failed to update personal information.\n' + str(e))
        # else:
        #     QMessageBox.warning(self, 'Invalid Input', 'Please enter valid name and age.')

    # dodelat image picker
    def add_picture(self):
        pass

    def createPatientsPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.patients_list = QListWidget()
        # rewrite to take from db
        # self.patients_list.addItem("John Doe, Flu")
        # self.patients_list.addItem("Jane Smith, Cold")
        self.loadNullPatients()
        self.patients_list.itemClicked.connect(self.patientClicked)
        layout.addWidget(self.patients_list)

        # self.addPatientButton = QPushButton("Add Patient")
        # layout.addWidget(self.addPatientButton)

        widget.setLayout(layout)
        return widget

    def loadNullPatients(self):
        self.patients_list.clear()
        patients = self.database.fetch_NULL_patients()
        if patients is None:
            QMessageBox.critical(self, 'Database Error', 'Failed to fetch appointments.')
            return

        for patient_id, name, birth, insurance in patients:
            date = birth.strftime("%Y-%m-%d")
            item_text = f"{name} Born: {date}, Insurance company: {insurance}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (patient_id, name))  # Store appointment ID and current status
            self.patients_list.addItem(item)

    def patientClicked(self, item):
        patient_id, name = item.data(Qt.UserRole)
        response = QMessageBox.question(self, 'Add Patient',
                                        f"Do you want to add {name} to your patients?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            # print("Delete patient functionality goes here.")
            self.database.add_doctor_to_patient(patient_id, self.doctor_id)
            self.loadPatients()
            self.loadAppointments()
            # db

    # patent picker
    def addPatient(self):
        print("Add patient functionality goes here.")

    def addAppointment(self):
        print("Add appointment functionality goes here.")
