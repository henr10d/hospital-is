from PyQt5 import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox,
                             QTextEdit, QTabWidget, QFormLayout, QFileDialog, QTimeEdit, QComboBox)
from PyQt5.QtWidgets import QDateEdit

from PyQt5.QtWidgets import QCalendarWidget, QDialog, QVBoxLayout
from PyQt5.QtCore import QDate

import mysql.connector
from DatabaseComms import DatabaseCommunicator


class PatientInterface(QWidget):

    def __init__(self, user_id, database: DatabaseCommunicator):
        super().__init__()
        self.user_id = user_id
        self.database = database
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Patient Dashboard')
        self.setGeometry(400, 400, 1280, 800)
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

        # Tab Widget for different sections
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.createPersonalInfoPage(), "Personal Info")
        self.tabWidget.addTab(self.createMedicalHistoryPage(), "Medical History")
        self.tabWidget.addTab(self.createAppointmentPage(), "Set Appointment")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)

    def createPersonalInfoPage(self):
        widget = QWidget()
        formLayout = QFormLayout()

        self.name_edit = QLineEdit()
        self.age_edit = QLineEdit()

        self.update_name_btn = QPushButton('Change Name')
        self.update_name_btn.clicked.connect(self.update_name)

        self.picture_label = QLabel()
        self.load_picture_btn = QPushButton('Add/Change Picture')
        self.load_picture_btn.clicked.connect(self.add_picture)

        formLayout.addRow("Name:", self.name_edit)
        formLayout.addRow("Age:", self.age_edit)
        formLayout.addRow(self.update_name_btn)
        formLayout.addRow("Picture:", self.picture_label)
        formLayout.addRow(self.load_picture_btn)

        widget.setLayout(formLayout)
        return widget

    def update_name(self):
        new_name = self.name_edit.text()
        # Here you can add code to update the name in the database
        QMessageBox.information(self, 'Name Changed', 'Your name has been updated successfully!')

    def update_age(self):
        new_age = self.age_edit.text()
        # Here you can add code to update the age in the database
        QMessageBox.information(self, 'Age Changed', 'Your age has been updated successfully!')

    def add_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Picture", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.picture_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            QMessageBox.information(self, 'Picture Updated', 'Your picture has been updated successfully!')

    def createMedicalHistoryPage(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Text area for medical history

        record = self.database.fetch_medical_record(self.user_id)
        if (record):
            self.medical_history_text = QTextEdit(record[0])
        else:
            self.medical_history_text = QTextEdit("")
        layout.addWidget(self.medical_history_text)

        # Button to update medical history
        self.update_history_btn = QPushButton('Update History')
        layout.addWidget(self.update_history_btn)
        self.update_history_btn.clicked.connect(self.update_medical_history)

        widget.setLayout(layout)
        return widget

    def update_medical_history(self):
        new_history = self.medical_history_text.toPlainText()
        result = self.database.fetch_medical_record(self.user_id)
        if result:
            self.database.update_medical_record((new_history, self.user_id))
        else:
            self.database.insert_medical_record((new_history, self.user_id))

        QMessageBox.information(self, 'Update Successful', 'Your medical history has been updated!')

    def createAppointmentPage(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Text area for appointments details
        self.appointment_info = QTextEdit()
        layout.addWidget(self.appointment_info)

        # Date picker for appointment time
        self.appointment_date_edit = QDateEdit()
        self.appointment_date_edit.setDate(QDate.currentDate())
        self.appointment_date_edit.setCalendarPopup(True)
        layout.addWidget(self.appointment_date_edit)

        # Button to add an appointment
        self.add_appointment_btn = QPushButton('Add Appointment')
        layout.addWidget(self.add_appointment_btn)
        # self.add_appointment_btn.clicked.connect(self.add_appointment)
        self.add_appointment_btn.clicked.connect(self.show_calendar)

        widget.setLayout(layout)
        return widget

    def show_calendar(self):
        self.calendar_dialog = QDialog(self)
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.setMaximumDate(QDate.currentDate().addYears(1))
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)

        hour_label = QLabel("Time:")
        layout.addWidget(hour_label)
        self.hour_combo = QComboBox()
        self.hour_combo.addItems([f"{i:02}" for i in range(24)])  # Hours from 00 to 23
        layout.addWidget(self.hour_combo)
        self.minute_combo = QComboBox()
        self.minute_combo.addItems([f"{i:02}" for i in range(0, 60, 15)])  # Minutes in increments of 15
        layout.addWidget(self.minute_combo)

        select_btn = QPushButton('Select Date and Time')
        select_btn.clicked.connect(self.add_appointment)
        layout.addWidget(select_btn)

        self.calendar_dialog.setLayout(layout)
        self.calendar_dialog.setWindowTitle('Select Date and Time for Appointment')
        self.calendar_dialog.exec_()

    def add_appointment(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        selected_hour = self.hour_combo.currentText()
        selected_minute = self.minute_combo.currentText()
        selected_time = f"{selected_hour}:{selected_minute}"
        appointment_details = self.appointment_info.toPlainText()
        full_details = f"{appointment_details} on {selected_date} at {selected_time}"
        self.database.add_appointment((self.user_id, full_details, selected_date, selected_time))
        QMessageBox.information(self, 'Appointment Added', 'Your appointment has been added successfully!')
        self.calendar_dialog.close()
