#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox,
                           QFrame, QComboBox, QFormLayout, QApplication, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from database import register_user, username_exists
from sql_utils import insert_pharmacist
from styles import StyleSheet

class RegistrationWindow(QMainWindow):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window

        self.setWindowTitle("Pharmacy Management System - Registration")
        self.setMinimumSize(800, 700)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(":/icons/pharmacy_logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel("New User\nRegistration")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")

        info_label = QLabel("Join our pharmacy management system\nComplete the form to create an account")
        info_label.setFont(QFont("Arial", 12))
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")

        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(title_label)
        left_layout.addSpacing(40)
        left_layout.addWidget(info_label)
        left_layout.addStretch()

        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)

        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_container.setMaximumWidth(450)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)

        form_title = QLabel("Create Account")
        form_title.setFont(QFont("Arial", 20, QFont.Bold))
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setStyleSheet("margin-bottom: 20px;")

        registration_form = QFormLayout()
        registration_form.setSpacing(15)
        registration_form.setLabelAlignment(Qt.AlignLeft)

        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter your full name")
        self.fullname_input.setMinimumHeight(40)
        registration_form.addRow("Full Name:", self.fullname_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setMinimumHeight(40)
        registration_form.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Choose a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        registration_form.addRow("Password:", self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(40)
        registration_form.addRow("Confirm Password:", self.confirm_password_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(40)
        registration_form.addRow("Email:", self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.phone_input.setMinimumHeight(40)
        registration_form.addRow("Phone:", self.phone_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Pharmacist", "Admin"])
        self.role_combo.setMinimumHeight(40)
        registration_form.addRow("Role:", self.role_combo)

        self.register_button = QPushButton("Create Account")
        self.register_button.setMinimumHeight(50)
        self.register_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.register_button.setObjectName("primaryButton")
        self.register_button.clicked.connect(self.register)

        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignCenter)
        back_text = QLabel("Already have an account?")
        back_link = QPushButton("Login")
        back_link.setFlat(True)
        back_link.setObjectName("linkButton")
        back_link.setCursor(Qt.PointingHandCursor)
        back_link.clicked.connect(self.back_to_login)
        back_layout.addWidget(back_text)
        back_layout.addWidget(back_link)

        form_layout.addWidget(form_title)
        form_layout.addLayout(registration_form)
        form_layout.addWidget(self.register_button)
        form_layout.addSpacing(20)
        form_layout.addLayout(back_layout)

        right_layout.addStretch()
        right_layout.addWidget(form_container)
        right_layout.addStretch()

        main_layout.addWidget(left_panel, 40)
        main_layout.addWidget(right_panel, 60)
        self.setCentralWidget(main_widget)

    def register(self):
        fullname = self.fullname_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        role = self.role_combo.currentText().lower()

        if not all([fullname, username, password, confirm_password, email, phone]):
            QMessageBox.warning(self, "Registration Failed", "Please fill in all fields.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Passwords do not match.")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Registration Failed", "Password must be at least 6 characters.")
            return
        if username_exists(username):
            QMessageBox.warning(self, "Registration Failed", "Username already exists. Please choose another one.")
            return

        if register_user(username, password, fullname, email, phone, role):
            QMessageBox.information(self, "Success", f"User {username} registered successfully.")
            self.back_to_login()
        else:
            QMessageBox.critical(self, "Error", "Registration failed.")

    def register_pharmacist(self):
        try:
            pharmacist_id = self.input_id.text()
            name = self.input_name.text()
            username = self.input_username.text()
            password = self.input_password.text()
            role = self.combo_role.currentText()
            insert_pharmacist(pharmacist_id, name, username, password, role)
            QMessageBox.information(self, "Success", "Pharmacist registered successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {e}")

    def create_pharmacist_registration_ui(self, role="admin"):
        if role != "admin":
            return
        form_box = QGroupBox("Register New Pharmacist")
        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Pharmacist ID")
        layout.addWidget(QLabel("Pharmacist ID:"))
        layout.addWidget(self.input_id)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Name")
        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.input_name)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.input_username)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.input_password)

        self.combo_role = QComboBox()
        self.combo_role.addItems(["admin", "pharmacist"])
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.combo_role)

        register_button = QPushButton("Register Pharmacist")
        register_button.clicked.connect(self.register_pharmacist)
        layout.addWidget(register_button)

        form_box.setLayout(layout)
        self.layout().addWidget(form_box)

    def back_to_login(self):
        if self.login_window:
            self.login_window.show()
        else:
            from login import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    reg_window = RegistrationWindow()
    reg_window.create_pharmacist_registration_ui(role="admin")
    reg_window.show()
    sys.exit(app.exec_())