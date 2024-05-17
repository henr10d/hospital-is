import mysql

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QLabel, QMessageBox,
                             QTextEdit, QTabWidget, QFormLayout, QFileDialog, QComboBox, QHBoxLayout, QSpacerItem,
                             QSizePolicy, QListWidgetItem, QListWidget, QDialogButtonBox)

from PyQt5.QtWidgets import QCalendarWidget, QDialog, QVBoxLayout
from PyQt5.QtCore import QDate, QBuffer, QByteArray

# import mysql.connector
from DatabaseComms import DatabaseCommunicator

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

    def fetch_picture(self, user_id):
        query = "SELECT image_path FROM users WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_personal_info(self, user_id, name, age):
        query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
        try:
            self.cursor.execute(query, (name, age, user_id))
            self.connection.commit()
            return True
        except Exception as e:
            print("Error updating personal info:", e)
            return False

    def fetch_personal_info(self, user_id):
        query = "SELECT name, age FROM users WHERE id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return None, None
        except Exception as e:
            print("Error fetching personal info:", e)
            return None, None



class PatientInterface(QWidget):

    def __init__(self, user_id, database: DatabaseCommunicator):
        super().__init__()
        self.user_id = user_id
        self.database = database
        self.initUI()

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
        self.tabWidget.addTab(self.createAppointmentPage(), "Set Appointment")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)

    def createPersonalInfoPage(self):
        self.database2 = Database()
        widget = QWidget()
        formLayout = QFormLayout()

        name, age = self.database2.fetch_personal_info(self.user_id)

        self.name_edit = QLineEdit(name if name is not None else '')
        # datum prepocet
        self.age_edit = QLineEdit(str(age) if age is not None else '')

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

        formLayout.addRow("Name:", self.name_edit)
        formLayout.addRow("Age:", self.age_edit)
        formLayout.addRow(update_btn_layout)
        # formLayout.addRow(self.picture_label)
        formLayout.addRow(picture_btn_layout)

        widget.setLayout(formLayout)
        return widget

    def update_personal_info(self):
        self.database2 = Database()


        new_name = self.name_edit.text()
        new_age = self.age_edit.text()
        if new_name and new_age:  # Simple validation
            try:
                self.database2.update_personal_info(self.user_id, new_name, new_age)
                QMessageBox.information(self, 'Update Successful',
                                        'Your personal information has been updated successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Update Failed', 'Failed to update personal information.\n' + str(e))
        else:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid name and age.')


    # def update_personal_info(self):
    #     new_name = self.name_edit.text()
    #     # Here you can add code to update the name in the database
    #     QMessageBox.information(self, 'Name Changed', 'Your name has been updated successfully!')

    # asi by to melo ukladat do filu projektu
    def add_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Picture", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            print(file_name)
            self.database2 = Database()


            self.database2.update_picture(self.user_id, file_name)
            QMessageBox.information(self, 'Picture Updated', 'Your picture has been updated successfully!')

            #¯\_(ツ)_/¯
            # Update the picture label
            # self.picture_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

            QMessageBox.information(self, 'Picture Updated', 'Your picture has been updated successfully!')

    def createMedicalHistoryPage(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.medical_history_list = QListWidget()

        # DB shrug
        medical_events = [
            ("2023-05-01", "Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
            ("2023-05-15", "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."),
            ("2023-06-03", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),
            ("2023-06-21", "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."),
            ("2023-07-04", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        ]

        for date, description in medical_events:
            item = QListWidgetItem(f"Date: {date} - Event: {description}")
            self.medical_history_list.addItem(item)

        layout.addWidget(self.medical_history_list)

        self.update_history_btn = QPushButton('Update History')
        history_btn_layout = QHBoxLayout()
        history_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        history_btn_layout.addWidget(self.update_history_btn)
        history_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(history_btn_layout)
        self.update_history_btn.clicked.connect(self.update_medical_history)

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
        layout = QVBoxLayout(widget)

        self.appointment_list = QListWidget()
        self.appointment_list.itemClicked.connect(self.show_appointment_details)

        # DB, date, text, status
        appointments = [
            ("2023-05-20 09:00", "Dental check-up", "approved"),
            ("2023-05-22 14:00", "General physician follow-up", "declined"),
            ("2023-05-30 16:00", "Orthopedic consultation", "waiting"),
            ("2023-06-05 10:00", "Cardiology exam", "approved"),
            ("2023-06-12 13:00", "Nutritionist appointment", "waiting")
        ]

        for time, description, status in appointments:
            if status == "approved":
                color = "\U0001F7E2"  # Green
            elif status == "declined":
                color = "\U0001F534"  # Red
            else:
                color = "\U0001F7E1"  # Yellow
            item = QListWidgetItem(f"{color} Time: {time} - Appointment: {description}")
            self.appointment_list.addItem(item)

        layout.addWidget(self.appointment_list)

        self.add_appointment_btn = QPushButton('Add New Appointment')
        self.add_appointment_btn.clicked.connect(self.show_calendar)  # Connect the button to the method
        appointment_btn_layout = QHBoxLayout()
        appointment_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        appointment_btn_layout.addWidget(self.add_appointment_btn)
        appointment_btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(appointment_btn_layout)

        legend_label = QLabel("🟢 Approved \U0001F7E1 Waiting 🔴 Declined")
        layout.addWidget(legend_label)

        return widget


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
