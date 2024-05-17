from PyQt5 import QtWidgets, QtCore, QtGui

# import MySQLdb
from hashlib import sha256
from PyQt5.QtWidgets import QMessageBox

from DoctorUI import DoctorInterface
from PatientUI import PatientInterface
from DatabaseComms import DatabaseCommunicator


class HospitalApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setWindowTitle("Login / Register")
        self.resize(400, 300)
        self.database = DatabaseCommunicator(
            "localhost",
            "root",
            "filip",
            "HospitalApp"
        )
        self.database.connect()

    def resizeEvent(self, event):
        new_font_size = max(12, min(24, self.width() // 30))
        font = QtGui.QFont("Arial", new_font_size)

        max_button_height = 50  # Maximum button height
        max_text_height = 40    # Maximum text field height
        max_width = 300         # Maximum width for buttons and text fields

        for widget in [self.username_input, self.password_input, self.role_input,
                       self.name_input, self.age_input, self.new_username_input,
                       self.new_password_input, self.new_role_input]:
            widget.setFont(font)
            widget.setMaximumSize(max_width, max_text_height)

        button_height = max(30, min(max_button_height, self.height() // 20))
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setFont(font)
            button.setMinimumHeight(button_height)
            button.setMaximumSize(max_width, max_button_height)

        super().resizeEvent(event)

    def setup_ui(self):

        self.stack = QtWidgets.QStackedWidget(self)
        self.stack.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # Login Form
        self.login_form = self.create_login_form()
        self.stack.addWidget(self.login_form)

        # Registration Form
        self.registration_form = self.create_registration_form()
        self.stack.addWidget(self.registration_form)

        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch()  # Adds a stretchable space before the stack
        layout.addWidget(self.stack)
        layout.addStretch()  # Adds a stretchable space after the stack
        # Styling
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
            }
            QLineEdit {
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
        """)

    def create_login_form(self):
        form = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(form)
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Aligns all widgets in the layout to the center

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(["Patient", "Doctor"])

        login_btn = QtWidgets.QPushButton("Login")
        login_btn.clicked.connect(self.login)

        register_btn = QtWidgets.QPushButton("Register")
        register_btn.clicked.connect(self.show_registration_form)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        return form

    def create_registration_form(self):
        form = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(form)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.age_input = QtWidgets.QLineEdit()
        self.age_input.setPlaceholderText("Age")
        self.age_input.setValidator(QtGui.QIntValidator(1, 100))
        self.new_username_input = QtWidgets.QLineEdit()
        self.new_username_input.setPlaceholderText("Username")
        self.new_password_input = QtWidgets.QLineEdit()
        self.new_password_input.setPlaceholderText("Password")
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_role_input = QtWidgets.QComboBox()
        self.new_role_input.addItems(["Patient", "Doctor", "Admin"])

        register_btn = QtWidgets.QPushButton("Register")
        register_btn.clicked.connect(self.register)

        back_btn = QtWidgets.QPushButton("Back to Login")
        back_btn.clicked.connect(self.show_login_form)

        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.new_username_input)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.new_role_input)
        layout.addWidget(register_btn)
        layout.addWidget(back_btn)

        return form

    def show_registration_form(self):
        self.stack.setCurrentIndex(1)

    def show_login_form(self):
        self.stack.setCurrentIndex(0)

    def open_role_interface(self, user_id):
        self.hide()
        if self.role_input.currentText().lower() == "doctor":
            self.interface = DoctorInterface(user_id, self.database)
        elif self.role_input.currentText().lower() == "patient":
            self.interface = PatientInterface(user_id, self.database)
        self.interface.show()

    def login(self):
        name = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText().lower()
        result = self.database.get_user_id((name, password, role))
        if result:
            QMessageBox.information(self, 'Login Success', f'Welcome {role} {name}!')
            self.open_role_interface(result)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid credentials or role!')

    def register(self):
        name = self.name_input.text()
        password = sha256(self.new_password_input.text().encode()).hexdigest()  # Hash the password
        role = self.new_role_input.currentText().lower()
        self.database.add_user_to_database((name, password, role))
