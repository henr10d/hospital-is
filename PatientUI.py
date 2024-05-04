import logging

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox,
                             QTextEdit, QTabWidget, QFormLayout)
import mysql.connector
from DoctorUI import DoctorInterface

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

        try:
            conn = self.connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT details FROM medical_history WHERE user_id = %s", (2,))

            # cursor.execute("SELECT id FROM medical_history WHERE user_id = %s", (2))
            xd = cursor.fetchone()
            print()
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            logging.exception(e)


        self.medical_history_text = QTextEdit(xd[0])
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

    # test
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
