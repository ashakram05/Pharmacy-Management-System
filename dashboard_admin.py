#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QFrame, QTabWidget, 
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QMessageBox, QDialog, QFormLayout, QLineEdit,
                           QComboBox, QApplication, QStackedWidget, QSplitter,
                           QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor

from database import get_all_users, add_medication, get_all_medications, delete_medication
from styles import StyleSheet


class AdminDashboard(QMainWindow):
    """
    Admin Dashboard for the Pharmacy Management System.
    Provides full access to system features and management capabilities.
    """
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        self.setWindowTitle("Pharmacy Management System - Admin Dashboard")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(StyleSheet.MAIN_STYLE + StyleSheet.DASHBOARD_STYLE)
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setObjectName("header")
        header.setMinimumHeight(60)
        header.setMaximumHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # App title
        app_title = QLabel("Pharmacy Management System")
        app_title.setFont(QFont("Arial", 16, QFont.Bold))
        
        # User info
        user_info = QLabel(f"Welcome, {self.user_data['fullname']} | Admin")
        user_info.setFont(QFont("Arial", 12))
        user_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.setFixedWidth(100)
        self.logout_button.clicked.connect(self.logout)
        
        # Add widgets to header layout
        header_layout.addWidget(app_title)
        header_layout.addStretch()
        header_layout.addWidget(user_info)
        header_layout.addWidget(self.logout_button)
        
        # Content area
        content_area = QFrame()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        # Navigation buttons
        self.nav_buttons = []
        
        nav_dashboard = QPushButton("Dashboard")
        nav_dashboard.setObjectName("navButton")
        nav_dashboard.setCheckable(True)
        nav_dashboard.setChecked(True)
        nav_dashboard.clicked.connect(lambda: self.change_page(0))
        sidebar_layout.addWidget(nav_dashboard)
        self.nav_buttons.append(nav_dashboard)
        
        nav_medications = QPushButton("Medications")
        nav_medications.setObjectName("navButton")
        nav_medications.setCheckable(True)
        nav_medications.clicked.connect(lambda: self.change_page(1))
        sidebar_layout.addWidget(nav_medications)
        self.nav_buttons.append(nav_medications)
        
        nav_users = QPushButton("Users")
        nav_users.setObjectName("navButton")
        nav_users.setCheckable(True)
        nav_users.clicked.connect(lambda: self.change_page(2))
        sidebar_layout.addWidget(nav_users)
        self.nav_buttons.append(nav_users)
        
        nav_reports = QPushButton("Reports")
        nav_reports.setObjectName("navButton")
        nav_reports.setCheckable(True)
        nav_reports.clicked.connect(lambda: self.change_page(3))
        sidebar_layout.addWidget(nav_reports)
        self.nav_buttons.append(nav_reports)
        
        nav_settings = QPushButton("Settings")
        nav_settings.setObjectName("navButton")
        nav_settings.setCheckable(True)
        nav_settings.clicked.connect(lambda: self.change_page(4))
        sidebar_layout.addWidget(nav_settings)
        self.nav_buttons.append(nav_settings)
        
        # Main content
        self.main_content = QStackedWidget()
        self.main_content.setObjectName("mainContent")
        
        # Dashboard page
        dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_page)
        
        # Dashboard title
        dashboard_title = QLabel("Admin Dashboard")
        dashboard_title.setFont(QFont("Arial", 20, QFont.Bold))
        dashboard_title.setContentsMargins(0, 0, 0, 20)
        
        # Dashboard cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Card 1: Total Users
        card1 = QFrame()
        card1.setObjectName("dashboardCard")
        card1_layout = QVBoxLayout(card1)
        
        card1_title = QLabel("Total Users")
        card1_title.setFont(QFont("Arial", 14))
        self.card1_value = QLabel("12")
        self.card1_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.card1_value.setAlignment(Qt.AlignCenter)
        
        card1_layout.addWidget(card1_title)
        card1_layout.addWidget(self.card1_value)
        cards_layout.addWidget(card1)
        
        # Card 2: Medications
        card2 = QFrame()
        card2.setObjectName("dashboardCard")
        card2_layout = QVBoxLayout(card2)
        
        card2_title = QLabel("Total Medications")
        card2_title.setFont(QFont("Arial", 14))
        self.card2_value = QLabel("342")
        self.card2_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.card2_value.setAlignment(Qt.AlignCenter)
        
        card2_layout.addWidget(card2_title)
        card2_layout.addWidget(self.card2_value)
        cards_layout.addWidget(card2)
        
        # Card 3: Pharmacists
        card3 = QFrame()
        card3.setObjectName("dashboardCard")
        card3_layout = QVBoxLayout(card3)
        
        card3_title = QLabel("Pharmacists")
        card3_title.setFont(QFont("Arial", 14))
        self.card3_value = QLabel("7")
        self.card3_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.card3_value.setAlignment(Qt.AlignCenter)
        
        card3_layout.addWidget(card3_title)
        card3_layout.addWidget(self.card3_value)
        cards_layout.addWidget(card3)
        
        # Card 4: Out of Stock
        card4 = QFrame()
        card4.setObjectName("dashboardCard")
        card4_layout = QVBoxLayout(card4)
        
        card4_title = QLabel("Out of Stock")
        card4_title.setFont(QFont("Arial", 14))
        card4_value = QLabel("15")
        card4_value.setFont(QFont("Arial", 24, QFont.Bold))
        card4_value.setAlignment(Qt.AlignCenter)
        
        card4_layout.addWidget(card4_title)
        card4_layout.addWidget(card4_value)
        cards_layout.addWidget(card4)
        
        # Recent Activity
        activity_frame = QFrame()
        activity_frame.setObjectName("activityFrame")
        activity_layout = QVBoxLayout(activity_frame)
        
        activity_title = QLabel("Recent Activity")
        activity_title.setFont(QFont("Arial", 16, QFont.Bold))
        
        activity_table = QTableWidget(5, 3)
        activity_table.setHorizontalHeaderLabels(["Time", "User", "Activity"])
        activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Sample data
        activities = [
            ["10:30 AM", "John (Pharmacist)", "Added medication: Amoxicillin 500mg"],
            ["09:45 AM", "Admin", "Created new user account: Sarah"],
            ["09:30 AM", "Lisa (Pharmacist)", "Updated inventory for Paracetamol"],
            ["Yesterday", "Admin", "Generated monthly sales report"],
            ["Yesterday", "Mike (Pharmacist)", "Completed stock verification"]
        ]
        
        for row, activity in enumerate(activities):
            for col, data in enumerate(activity):
                item = QTableWidgetItem(data)
                if col == 0:
                    item.setFont(QFont("Arial", 10, QFont.Bold))
                activity_table.setItem(row, col, item)
        
        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(activity_table)
        
        # Add widgets to dashboard layout
        dashboard_layout.addWidget(dashboard_title)
        dashboard_layout.addLayout(cards_layout)
        dashboard_layout.addWidget(activity_frame)
        
        # Medications page
        medications_page = QWidget()
        medications_layout = QVBoxLayout(medications_page)
        
        # Medications header
        medications_header = QHBoxLayout()
        medications_title = QLabel("Medications Management")
        medications_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        add_med_button = QPushButton("Add New Medication")
        add_med_button.setObjectName("primaryButton")
        add_med_button.setMinimumHeight(40)
        add_med_button.clicked.connect(self.add_new_medication)
        
        medications_header.addWidget(medications_title)
        medications_header.addStretch()
        medications_header.addWidget(add_med_button)
        
        # Medications table
        self.medications_table = QTableWidget()
        self.medications_table.setObjectName("dataTable")
        self.medications_table.setColumnCount(6)
        self.medications_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Stock", "Price", "Actions"])
        self.medications_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.medications_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.medications_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        # Load medications data
        self.load_medications_data()
        
        # Add widgets to medications layout
        medications_layout.addLayout(medications_header)
        medications_layout.addWidget(self.medications_table)
        
        # Users page
        users_page = QWidget()
        users_layout = QVBoxLayout(users_page)
        
        # Users header
        users_header = QHBoxLayout()
        users_title = QLabel("User Management")
        users_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        users_header.addWidget(users_title)
        users_header.addStretch()
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setObjectName("dataTable")
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Name", "Username", "Role", "Status"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Load users data
        self.load_users_data()
        
        # Add widgets to users layout
        users_layout.addLayout(users_header)
        users_layout.addWidget(self.users_table)
        
        # Reports page
        reports_page = QWidget()
        reports_layout = QVBoxLayout(reports_page)
        
        # Reports title
        reports_title = QLabel("Reports")
        reports_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        # Reports tabs
        reports_tabs = QTabWidget()
        reports_tabs.setObjectName("contentTabs")
        
        # Sales report tab
        sales_tab = QWidget()
        sales_layout = QVBoxLayout(sales_tab)
        
        sales_info = QLabel("Sales reports and analytics will be displayed here.")
        sales_info.setAlignment(Qt.AlignCenter)
        sales_layout.addWidget(sales_info)
        
        reports_tabs.addTab(sales_tab, "Sales Reports")
        
        # Inventory report tab
        inventory_tab = QWidget()
        inventory_layout = QVBoxLayout(inventory_tab)
        
        inventory_info = QLabel("Inventory status and details will be displayed here.")
        inventory_info.setAlignment(Qt.AlignCenter)
        inventory_layout.addWidget(inventory_info)
        
        reports_tabs.addTab(inventory_tab, "Inventory Reports")
        
        # User activity report tab
        activity_tab = QWidget()
        activity_tab_layout = QVBoxLayout(activity_tab)
        
        activity_info = QLabel("User activity logs will be displayed here.")
        activity_info.setAlignment(Qt.AlignCenter)
        activity_tab_layout.addWidget(activity_info)
        
        reports_tabs.addTab(activity_tab, "User Activity")
        
        # Add widgets to reports layout
        reports_layout.addWidget(reports_title)
        reports_layout.addWidget(reports_tabs)
        
        # Settings page
        settings_page = QWidget()
        settings_layout = QVBoxLayout(settings_page)
        
        # Settings title
        settings_title = QLabel("System Settings")
        settings_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        # Settings content
        settings_content = QFrame()
        settings_content.setObjectName("settingsFrame")
        settings_form = QFormLayout(settings_content)
        settings_form.setVerticalSpacing(20)
        
        # Company name
        company_name = QLineEdit("ABC Pharmacy")
        company_name.setMinimumHeight(40)
        settings_form.addRow("Company Name:", company_name)
        
        # Address
        address = QLineEdit("123 Main Street, City, Country")
        address.setMinimumHeight(40)
        settings_form.addRow("Address:", address)
        
        # Email
        email = QLineEdit("contact@abcpharmacy.com")
        email.setMinimumHeight(40)
        settings_form.addRow("Email:", email)
        
        # Phone
        phone = QLineEdit("+1 234 567 8900")
        phone.setMinimumHeight(40)
        settings_form.addRow("Phone:", phone)
        
        # Tax Rate
        tax_rate = QLineEdit("7.5%")
        tax_rate.setMinimumHeight(40)
        settings_form.addRow("Tax Rate:", tax_rate)
        
        # Currency
        currency = QComboBox()
        currency.addItems(["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)"])
        currency.setMinimumHeight(40)
        settings_form.addRow("Currency:", currency)
        
        # Save button
        save_settings = QPushButton("Save Settings")
        save_settings.setObjectName("primaryButton")
        save_settings.setMinimumHeight(50)
        save_settings.setMaximumWidth(200)
        
        # Add widgets to settings layout
        settings_layout.addWidget(settings_title)
        settings_layout.addWidget(settings_content)
        settings_layout.addWidget(save_settings, alignment=Qt.AlignHCenter)
        settings_layout.addStretch()
        
        # Add pages to stacked widget
        self.main_content.addWidget(dashboard_page)
        self.main_content.addWidget(medications_page)
        self.main_content.addWidget(users_page)
        self.main_content.addWidget(reports_page)
        self.main_content.addWidget(settings_page)
        
        # Add sidebar and main content to content area
        content_layout.addWidget(sidebar)
        content_layout.addWidget(self.main_content)
        
        # Add header and content area to main layout
        main_layout.addWidget(header)
        main_layout.addWidget(content_area)
        
        # Set central widget
        self.setCentralWidget(main_widget)
    
    def change_page(self, index):
        """
        Change the active page in the dashboard
        """
        # Update the active navigation button
        for i, button in enumerate(self.nav_buttons):
            if i == index:
                button.setChecked(True)
            else:
                button.setChecked(False)
        
        # Switch to the selected page
        self.main_content.setCurrentIndex(index)
    
    def load_medications_data(self):
        """
        Load medications data from the database
        """
        medications = get_all_medications()
        
        self.medications_table.setRowCount(len(medications))
        
        for row, med in enumerate(medications):
            # ID
            id_item = QTableWidgetItem(str(med['id']))
            self.medications_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(med['name'])
            self.medications_table.setItem(row, 1, name_item)
            
            # Category
            category_item = QTableWidgetItem(med['category'])
            self.medications_table.setItem(row, 2, category_item)
            
            # Stock
            stock_item = QTableWidgetItem(str(med['stock']))
            self.medications_table.setItem(row, 3, stock_item)
            
            # Price
            price_item = QTableWidgetItem(f"${med['price']:.2f}")
            self.medications_table.setItem(row, 4, price_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(5)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("editButton")
            edit_btn.setMaximumWidth(60)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("deleteButton")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda _, med_id=med['id']: self.delete_medication(med_id))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.medications_table.setCellWidget(row, 5, actions_widget)
    
    def add_new_medication(self):
        """
        Show dialog to add a new medication
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Medication")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet(StyleSheet.DIALOG_STYLE)
        
        layout = QVBoxLayout(dialog)
        
        # Form
        form = QFormLayout()
        form.setVerticalSpacing(15)
        
        # Name
        name_input = QLineEdit()
        name_input.setMinimumHeight(40)
        form.addRow("Name:", name_input)
        
        # Description
        description_input = QLineEdit()
        description_input.setMinimumHeight(40)
        form.addRow("Description:", description_input)
        
        # Category
        category_input = QComboBox()
        category_input.addItems(["Antibiotics", "Analgesics", "Antivirals", "Cardiovascular", "Diabetic", "Other"])
        category_input.setMinimumHeight(40)
        form.addRow("Category:", category_input)
        
        # Stock
        stock_input = QLineEdit()
        stock_input.setMinimumHeight(40)
        form.addRow("Initial Stock:", stock_input)
        
        # Price
        price_input = QLineEdit()
        price_input.setMinimumHeight(40)
        form.addRow("Price ($):", price_input)
        
        # Add form to layout
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        
        save_button = QPushButton("Save Medication")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(lambda: self.save_new_medication(
            name_input.text(),
            description_input.text(),
            category_input.currentText(),
            stock_input.text(),
            price_input.text(),
            dialog
        ))
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_new_medication(self, name, description, category, stock, price, dialog):
        """
        Save a new medication to the database
        """
        # Validate inputs
        if not name or not stock or not price:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all required fields.")
            return
        
        try:
            stock = int(stock)
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Stock must be a whole number and price must be a number.")
            return
        
        # Add medication to database
        add_medication(name, description, category, stock, price)
        
        # Reload medications data
        self.load_medications_data()
        
        # Close dialog
        dialog.accept()
    
    def delete_medication(self, med_id):
        """
        Delete a medication from the database
        """
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion",
            "Are you sure you want to delete this medication? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete from database
            delete_medication(med_id)
            
            # Reload medications data
            self.load_medications_data()
    
    def load_users_data(self):
        """
        Load users data from the database
        """
        users = get_all_users()
        
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # ID
            id_item = QTableWidgetItem(str(user['id']))
            self.users_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(user['fullname'])
            self.users_table.setItem(row, 1, name_item)
            
            # Username
            username_item = QTableWidgetItem(user['username'])
            self.users_table.setItem(row, 2, username_item)
            
            # Role
            role_item = QTableWidgetItem(user['role'].capitalize())
            self.users_table.setItem(row, 3, role_item)
            
            # Status
            status = "Active" if user['active'] else "Inactive"
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor("#4CAF50") if status == "Active" else QColor("#F44336"))
            self.users_table.setItem(row, 4, status_item)
    
    def logout(self):
        """
        Logout user and return to login screen
        """
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


# For testing purposes
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    user = {
        'id': 1,
        'username': 'admin',
        'fullname': 'Admin User',
        'role': 'admin'
    }
    dashboard = AdminDashboard(user)
    dashboard.show()
    sys.exit(app.exec_())
