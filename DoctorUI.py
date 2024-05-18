import mysql
# from PyQt5 import Qt
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QTabWidget, QFormLayout, \
    QLineEdit, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidgetItem


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='filip',
            database='HospitalApp'
        )
        self.cursor = self.connection.cursor()

    def update_picture(self, user_id, image_path):
        query = "UPDATE users SET image_path = %s WHERE id = %s"
        self.cursor.execute(query, (image_path, user_id))
        self.connection.commit()


    def get_doctor_id_by_user_id(self, user_id):
        query = "SELECT doctor_id FROM doctors WHERE user_id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print("Error fetching doctor_id:", e)
            return None

    def fetch_appointments_for_doctor(self, doctor_id):
        query = """
        SELECT patient_id, appointment_time, appointment_details, status 
        FROM appointments 
        WHERE doctor_id = %s
        ORDER BY appointment_time DESC
        """
        try:
            self.cursor.execute(query, (doctor_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print("Error fetching appointments:", e)
            return []

    def update_appointment_status(self, id, new_status):
        query = "UPDATE appointments SET status = %s WHERE id = %s"
        try:
            self.cursor.execute(query, (new_status, id))
            self.connection.commit()
        except Exception as e:
            print("Error updating appointment status:", e)



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

    def loadAppointments(self):
        self.appointment_list.clear()  # Clear existing items before loading new ones
        self.database2 = Database()

        doctor_id = self.database2.get_doctor_id_by_user_id(self.user_id)
        if not doctor_id:
            QMessageBox.critical(self, 'Database Error', 'Failed to find associated doctor ID.')
            return

        appointments = self.database2.fetch_appointments_for_doctor(doctor_id)
        if not appointments:
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


    def appointmentClicked(self, item):
        appointment_id, current_status = item.data(Qt.UserRole)
        new_status = 'approved' if current_status != 'approved' else 'declined'
        response = QMessageBox.question(self, 'Change Appointment Status',
                                        f"Do you want to change the appointment status to {'Approved' if new_status == 'approved' else 'Declined'}?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            # self.database.update_appointment_status(appointment_id, new_status)
            QMessageBox.information(self, 'Status Updated',
                                    f'Appointment status has been changed to {"Approved" if new_status == "approved" else "Declined"}.')
            # Refresh the list or update the item directly here to show new status
        self.loadAppointments()

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

    def appointmentClicked(self, item):
        appointment_id, current_status = item.data(Qt.UserRole)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Change Appointment Status")
        msg_box.setText("Choose the new status for this appointment:")
        msg_box.addButton('Approve', QMessageBox.AcceptRole)
        msg_box.addButton('Decline', QMessageBox.RejectRole)
        msg_box.addButton(QMessageBox.Cancel)

        result = msg_box.exec_()

        if result == QMessageBox.AcceptRole:
            new_status = 'approved'
        elif result == QMessageBox.RejectRole:
            new_status = 'declined'
        else:
            return  # Do nothing if Cancel is clicked

        # Update the appointment status in the database
        self.database2 = Database()

        self.database2.update_appointment_status(appointment_id, new_status)

        QMessageBox.information(self, 'Status Updated',
                                f'Appointment status has been changed to {"Approved" if new_status == "approved" else "Declined"}.')
        self.loadAppointments()
        # add page refres


    def addAppointment(self):
        print("Add appointment functionality goes here.")
