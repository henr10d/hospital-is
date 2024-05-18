from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QLabel, QMessageBox,
                             QTextEdit, QTabWidget, QFormLayout, QFileDialog, QComboBox, QHBoxLayout, QSpacerItem,
                             QSizePolicy, QListWidgetItem, QListWidget, QDialogButtonBox)

from PyQt5.QtWidgets import QCalendarWidget, QDialog, QVBoxLayout
from PyQt5.QtCore import QDate, QTimer, Qt
from hashlib import sha256

from DatabaseComms import DatabaseCommunicator

class PatientInterface(QWidget):

    def __init__(self, patient, database: DatabaseCommunicator, username):
        super().__init__()
        self.patient_id = patient[0]
        self.doctor_id = patient[1]
        self.patient_name = patient[3]
        self.patient_birth = patient[4]
        self.insurance = patient[5]
        self.database = database
        self.username = username
        self.initUI()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_appointments)
        self.refresh_timer.start(1000)

    def initUI(self):
        self.setWindowTitle('Patient Dashboard')
        self.setGeometry(400, 400, 1280, 800)
        # Inside the initUI method or wherever you define these buttons

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
        self.tabWidget.addTab(self.createAppointmentPage(), "Appointments")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)

    def createAppointmentPage(self):

        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.appointment_list = QListWidget()
        self.appointment_list.itemClicked.connect(self.show_appointment_details)

        self.refresh_appointments()

        layout.addWidget(self.appointment_list)

        self.add_appointment_btn = QPushButton('Add New Appointment')
        self.add_appointment_btn.clicked.connect(self.show_calendar)
        appointment_btn_layout = QHBoxLayout()
        appointment_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        appointment_btn_layout.addWidget(self.add_appointment_btn)
        appointment_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(appointment_btn_layout)

        legend_label = QLabel("🟢 Approved \U0001F7E1 Waiting 🔴 Declined")
        layout.addWidget(legend_label)

        return widget
    
    def refresh_appointments(self):
        appointments = self.database.fetch_patient_appointments(self.patient_id)

        if len(appointments) == len(self.appointment_list):
            return

        self.appointment_list.clear()

        if appointments is not None:
            for id, time, description, status in appointments:
                if status == "approved":
                    color = "\U0001F7E2"  # Green
                elif status == "declined":
                    color = "\U0001F534"  # Red
                else:
                    color = "\U0001F7E1"  # Yellow
                item = QListWidgetItem(f"{color} Time: {time} - Appointment: {description}")
                item.setData(Qt.UserRole, id)
                self.appointment_list.addItem(item)

    def createPersonalInfoPage(self):
        widget = QWidget()
        layout = QFormLayout()

        nameLabel = QLabel(self.patient_name if self.patient_name is not None else '')
        ageLabel = QLabel(self.patient_birth.strftime("%Y-%m-%d") if self.patient_birth is not None else '')
        self.username_edit = QLineEdit(self.username if self.username is not None else '')
        self.password_edit = QLineEdit('')
        # datum prepocet
        # self.age_edit = QLineEdit(str(self.patient_birth) if self.patient_birth is not None else '')

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
        # formLayout.addRow(self.picture_label)
        layout.addRow(picture_btn_layout)

        widget.setLayout(layout)
        return widget

    def update_personal_info(self):
        new_username = self.username_edit.text()
        new_password = self.password_edit.text()
        if new_username is None or new_username == '' or new_password is None or new_password == '':
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid non empty username and password.')
            return
        self.username = new_username
        password = sha256(new_password.encode()).hexdigest()

        try:
            self.database.update_login_credentials((self.username, password, self.patient_id))
            QMessageBox.information(self, 'Update Successful',
                                    'Your personal information has been updated successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Update Failed', 'Failed to update personal information.\n' + str(e))
        # else:
        #     QMessageBox.warning(self, 'Invalid Input', 'Please enter valid name and age.')


    # asi by to melo ukladat do filu projektu
    def add_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Picture", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            print(file_name)

            self.database.update_patient_picture(self.patient_id, file_name)
            QMessageBox.information(self, 'Picture Updated', 'Your picture has been updated successfully!')

            #¯\_(ツ)_/¯
            # Update the picture label
            # self.picture_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

            QMessageBox.information(self, 'Picture Updated', 'Your picture has been updated successfully!')

    def createMedicalHistoryPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.medical_history_list = QListWidget()

        medical_records = self.database.fetch_patient_medical_records(self.patient_id)
        if medical_records is None:
            QMessageBox.critical(self, 'Database Error', 'Failed to fetch medical history.')
            return widget

        for event in medical_records:
            date, description = event
            item = QListWidgetItem(f"Date: {date} - Event: {description}")
            self.medical_history_list.addItem(item)

        layout.addWidget(self.medical_history_list)

        self.update_history_btn = QPushButton('Update History')
        history_btn_layout = QHBoxLayout()
        history_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        history_btn_layout.addWidget(self.update_history_btn)
        history_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(history_btn_layout)
        self.reload_medical_history()

        self.update_history_btn.clicked.connect(self.update_medical_history)

        return widget

    def reload_medical_history(self):
        self.medical_history_list.clear()  # Clear existing items

        medical_records = self.database.fetch_patient_medical_records(self.patient_id)
        if medical_records is None:
            QMessageBox.critical(self, 'Database Error', 'Failed to fetch medical history.')
        else:
            for date, description in medical_records:
                item = QListWidgetItem(f"Date: {date} - Event: {description}")
                self.medical_history_list.addItem(item)

    def update_medical_history(self):
        # Creating a dialog for entering new medical history
        self.history_dialog = QDialog(self)
        self.history_dialog.setWindowTitle('Update Medical History')
        layout = QVBoxLayout(self.history_dialog)

        # Adding a text edit field to enter new history
        self.medical_history_text = QTextEdit()
        self.medical_history_text.setPlaceholderText("Enter new medical history details...")
        layout.addWidget(self.medical_history_text)

        # Adding a button box for submitting or cancelling
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        button_box.accepted.connect(self.submit_medical_history)
        button_box.rejected.connect(self.history_dialog.reject)

        self.history_dialog.setLayout(layout)
        self.history_dialog.exec_()

    def submit_medical_history(self):

        new_history = self.medical_history_text.toPlainText()
        if new_history.strip():
            self.database2.insert_medical_record(self.user_id, new_history)
            self.reload_medical_history()

            QMessageBox.information(self, 'Update Successful', 'Your medical history has been updated!')
            self.history_dialog.accept()
        else:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid medical history details.')


    def show_appointment_details(self, item):
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle('Appointment Details')
        layout = QVBoxLayout(details_dialog)

        label = QLabel(f"Details for the selected appointment:\n{item.text()}")
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Close)
        button_box.accepted.connect(details_dialog.accept)
        button_box.rejected.connect(details_dialog.reject)
        layout.addWidget(button_box)

        button_box.button(QDialogButtonBox.Cancel).clicked.connect(lambda: self.cancel_appointment(item))

        details_dialog.setLayout(layout)
        details_dialog.exec_()

    def cancel_appointment(self, item):
        # hehe
        self.database.cancel_appointment((item.data(Qt.UserRole), ))
        self.appointment_list.takeItem(self.appointment_list.row(item))
        QMessageBox.information(self, 'Appointment Cancelled', 'The appointment has been successfully cancelled!')

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
        self.hour_combo.addItems([f"{i:02}" for i in range(24)])
        layout.addWidget(self.hour_combo)
        self.minute_combo = QComboBox()
        self.minute_combo.addItems([f"{i:02}" for i in range(0, 60, 15)])
        layout.addWidget(self.minute_combo)
        info_label = QLabel("Appointment info:")
        layout.addWidget(info_label)
        self.appointment_info = QLineEdit()
        layout.addWidget(self.appointment_info)

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
        selected_datetime = selected_date + " " + selected_time + ":00"
        full_details = f"{self.appointment_info.text()} on {selected_date} at {selected_time}"
        print(full_details)
        self.database.add_appointment((self.patient_id, self.doctor_id, full_details, selected_datetime, "waiting"))
        QMessageBox.information(self, 'Appointment Added', 'Your appointment has been added successfully!')
        self.calendar_dialog.close()
