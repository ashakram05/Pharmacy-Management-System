#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox,
                           QFrame, QSizePolicy, QApplication)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont

from database import authenticate_user
from styles import StyleSheet
from dashboard_admin import AdminDashboard
from dashboard_pharmacist import PharmacistDashboard
from registration import RegistrationWindow

class LoginWindow(QMainWindow):
    """
    Login window for the Pharmacy Management System.
    Handles user authentication and redirects to appropriate dashboard based on role.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Pharmacy Management System - Login")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # Create left panel (logo and info)
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(":/icons/pharmacy_logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("MediTracx\nLogin Portal")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")
        
        # Info text
        info_label = QLabel("Secure Access Portal\nPlease login to continue")
        info_label.setFont(QFont("Arial", 12))
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        
        # Add widgets to left layout
        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(title_label)
        left_layout.addSpacing(40)
        left_layout.addWidget(info_label)
        left_layout.addStretch()
        
        # Create right panel (login form)
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # Login form container
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_container.setMaximumWidth(400)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # Form title
        form_title = QLabel("Login")
        form_title.setFont(QFont("Arial", 20, QFont.Bold))
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setStyleSheet("margin-bottom: 20px;")
        
        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Arial", 12))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(40)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(50)
        self.login_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.login_button.setObjectName("primaryButton")
        self.login_button.clicked.connect(self.authenticate)
        
        # Register link
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignCenter)
        register_text = QLabel("Don't have an account?")
        register_link = QPushButton("Register Now")
        register_link.setFlat(True)
        register_link.setObjectName("linkButton")
        register_link.setCursor(Qt.PointingHandCursor)
        register_link.clicked.connect(self.open_registration)
        register_layout.addWidget(register_text)
        register_layout.addWidget(register_link)
        
        # Add widgets to form layout
        form_layout.addWidget(form_title)
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addSpacing(20)
        form_layout.addLayout(register_layout)
        
        # Add form to right layout
        right_layout.addStretch()
        right_layout.addWidget(form_container)
        right_layout.addStretch()
        
        # Set panel sizes
        main_layout.addWidget(left_panel, 40)
        main_layout.addWidget(right_panel, 60)
        
        # Set main widget
        self.setCentralWidget(main_widget)
        
    def authenticate(self):
        """
        Authenticate user credentials and redirect to appropriate dashboard
        """
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Check for empty fields
        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
            return
            
        # Authenticate user
        user = authenticate_user(username, password)
        
        if user:
            self.hide()
            
            # Open appropriate dashboard based on role
            if user['role'] == 'admin':
                self.admin_dashboard = AdminDashboard(user)
                self.admin_dashboard.show()
            elif user['role'] == 'pharmacist':
                self.pharmacist_dashboard = PharmacistDashboard(user)
                self.pharmacist_dashboard.show()
                
            # Clear login fields
            self.username_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
    
    def open_registration(self):
        """
        Open the registration window
        """
        self.registration_window = RegistrationWindow(self)
        self.registration_window.show()
        self.hide()


# For testing purposes
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())