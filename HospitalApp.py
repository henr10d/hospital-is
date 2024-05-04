from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
                             QHBoxLayout, QComboBox, QFormLayout)
from PyQt5.QtGui import QFont
from DoctorUI import DoctorInterface
from PatientUI import PatientInterface

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
