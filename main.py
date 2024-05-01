import sys
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox,
                             QHBoxLayout, QComboBox, QTextEdit, QTabWidget, QFormLayout)
from PyQt5.QtGui import QFont

import mysql.connector

class HospitalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hospital App')
        self.setGeometry(400, 400, 1280, 800)
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout(self)

        # Credentials layout
        self.credentials_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(["Doctor", "Patient"])
        self.credentials_layout.addRow("Name:", self.name_input)
        self.credentials_layout.addRow("Password:", self.password_input)
        self.credentials_layout.addRow("Role:", self.role_input)
        self.layout.addLayout(self.credentials_layout)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.login_button = QPushButton('Login')
        self.register_button = QPushButton('Register')
        self.buttons_layout.addWidget(self.login_button)
        self.buttons_layout.addWidget(self.register_button)
        self.layout.addLayout(self.buttons_layout)

        # Styling buttons
        self.styleButtons()

        # Connect buttons
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def styleButtons(self):
        self.login_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; }"
                                        "QPushButton:hover { background-color: #45a049; }")
        self.register_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 10px; }"
                                           "QPushButton:hover { background-color: #1976D2; }")

    def register(self):
        name = self.name_input.text()
        password = self.password_input.text()  # Consider hashing this password before storing
        role = self.role_input.currentText().lower()
        conn = self.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, password, role) VALUES (%s, %s, %s)", (name, password, role))
        conn.commit()
        cursor.close()
        conn.close()
        QMessageBox.information(self, 'Register Success', 'You are registered successfully!')

    def login(self):
        name = self.name_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText().lower()
        conn = self.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = %s AND password = %s AND role = %s", (name, password, role))
        result = cursor.fetchone()
        if result:
            QMessageBox.information(self, 'Login Success', f'Welcome {role} {name}!')
            self.open_role_interface(role)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid credentials or role!')
        cursor.close()
        conn.close()

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",  # Or the relevant host where your MySQL server is running
            user="root",  # Replace with your MySQL user
            password="filip",  # Replace with your MySQL password
            database="HospitalApp"
        )


    # def login(self):
    #     name = self.name_input.text()
    #     password = self.password_input.text()
    #     role = self.role_input.currentText().lower()
    #     with open("users.txt", "r") as file:
    #         for line in file:
    #             reg_name, reg_pass, reg_role = line.strip().split(',')
    #             if reg_name == name and reg_pass == password and reg_role == role:
    #                 QMessageBox.information(self, 'Login Success', f'Welcome {role} {name}!')
    #                 self.open_role_interface(role)
    #                 return
    #         QMessageBox.warning(self, 'Login Failed', 'Invalid credentials or role!')
    #
    # def register(self):
    #     name = self.name_input.text()
    #     password = self.password_input.text()
    #     role = self.role_input.currentText().lower()
    #     with open("users.txt", "a") as file:
    #         file.write(f"{name},{password},{role}\n")
    #     QMessageBox.information(self, 'Register Success', 'You are registered successfully!')

    def open_role_interface(self, role):
        self.hide()
        if role == "doctor":
            self.interface = DoctorInterface()
        elif role == "patient":
            self.interface = PatientInterface()
        self.interface.show()

    def resizeEvent(self, event):
        # Apply a more subtle scaling of font size
        new_font_size = max(8, min(12, self.width() // 100 + self.height() // 150))
        font = QFont("Arial", new_font_size)
        self.applyFontChange(font)

    def applyFontChange(self, font):
        self.name_input.setFont(font)
        self.password_input.setFont(font)
        self.role_input.setFont(font)
        self.login_button.setFont(font)
        self.register_button.setFont(font)


class DoctorInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Doctor Dashboard')
        self.setGeometry(400, 400, 1280, 800)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.patients_list = QTextEdit("Patients' List:\nJohn Doe, Flu\nJane Smith, Cold")
        self.appointments = QTextEdit("Today's Appointments:\nJohn Doe at 10:00 AM\nJane Smith at 11:00 AM")
        layout.addWidget(self.patients_list)
        layout.addWidget(self.appointments)


class PatientInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Patient Dashboard')
        self.setGeometry(400, 400, 1280, 800)
        self.initUI()

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",  # Or the relevant host where your MySQL server is running
            user="root",  # Replace with your MySQL user
            password="filip",  # Replace with your MySQL password
            database="HospitalApp"
        )

    def initUI(self):
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.createPersonalInfoPage(), "Personal Info")
        self.tabWidget.addTab(self.createMedicalHistoryPage(), "Medical History")
        self.tabWidget.addTab(self.createAppointmentPage(), "Set Appointment")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)

    def createPersonalInfoPage(self):
        widget = QWidget()
        formLayout = QFormLayout()
        name_edit = QLineEdit()
        age_edit = QLineEdit()
        formLayout.addRow("Name:", name_edit)
        formLayout.addRow("Age:", age_edit)
        # Example of adding a picture
        pixmap = QPixmap(100, 100)
        pixmap.fill()
        picture_label = QLabel()
        picture_label.setPixmap(pixmap)
        formLayout.addRow("Picture:", picture_label)
        widget.setLayout(formLayout)
        return widget

    def createMedicalHistoryPage(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Text area for medical history


        # conn = self.connect_to_database()
        # cursor = conn.cursor()
        # cursor.execute("SELECT id FROM medical_history WHERE user_id = %s", (2))
        # xd = cursor.fetchone()
        # print()
        # conn.commit()
        # cursor.close()
        # conn.close()


        self.medical_history_text = QTextEdit("co to je wtf omg")
        layout.addWidget(self.medical_history_text)

        # Button to update medical history
        self.update_history_btn = QPushButton('Update History')
        layout.addWidget(self.update_history_btn)
        self.update_history_btn.clicked.connect(self.update_medical_history)

        widget.setLayout(layout)
        return widget

    def update_medical_history(self):
        print("xd")
        # Assuming user_id is accessible as self.user_id
        new_history = self.medical_history_text.toPlainText()
        conn = self.connect_to_database()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO users (name, password, role) VALUES (%s, %s, %s)", (name, password, role))
        cursor.execute("INSERT into medical_history values(%s,%s,%s)", (new_history, self.user_id))

        # cursor.execute("INSERT or UPDATE medical_history SET details = %s WHERE user_id = %s", (new_history, self.user_id))
        conn.commit()
        cursor.close()
        conn.close()
        QMessageBox.information(self, 'Update Successful', 'Your medical history has been updated!')

    # def createMedicalHistoryPage(self):
    #     widget = QWidget()
    #     layout = QVBoxLayout()
    #     medical_history = QTextEdit("No medical history available.")
    #     layout.addWidget(medical_history)
    #     widget.setLayout(layout)
    #     return widget

    def createAppointmentPage(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Text area for appointments
        self.appointment_info = QTextEdit()
        layout.addWidget(self.appointment_info)

        # Button to add an appointment
        self.add_appointment_btn = QPushButton('Add Appointment')
        layout.addWidget(self.add_appointment_btn)
        self.add_appointment_btn.clicked.connect(self.add_appointment)

        widget.setLayout(layout)
        return widget

    def add_appointment(self):
        # Retrieve appointment details from the text area
        appointment_details = self.appointment_info.toPlainText()
        appointment_time = ...  # You need to define a way to get this, possibly from another input field

        conn = self.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointments (user_id, appointment_details, appointment_time) VALUES (%s, %s, %s)",
                       (self.user_id, appointment_details, appointment_time))
        conn.commit()
        cursor.close()
        conn.close()
        QMessageBox.information(self, 'Appointment Added', 'Your appointment has been added successfully!')


    # def createAppointmentPage(self):
    #     widget = QWidget()
    #     layout = QVBoxLayout()
    #     appointment_info = QTextEdit("No appointments set.")
    #     layout.addWidget(appointment_info)
    #     widget.setLayout(layout)
    #     return widget

    def open_role_interface(self, role):
        self.hide()
        if role == "doctor":
            self.interface = DoctorInterface()
        elif role == "patient":
            self.interface = PatientInterface()
        self.interface.showFullScreen()  # Changed from show() to showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HospitalApp()
    ex.show()
    # ex.showFullScreen()
    sys.exit(app.exec_())
