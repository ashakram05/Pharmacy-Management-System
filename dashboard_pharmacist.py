#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QFrame, QTabWidget, 
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QMessageBox, QDialog, QFormLayout, QLineEdit,
                           QComboBox, QApplication, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QColor

from database import get_all_medications, get_medication_by_id, update_medication_stock
from sql_connection import DatabaseConnection
from styles import StyleSheet


class PharmacistDashboard(QMainWindow):
    """
    Pharmacist Dashboard for the Pharmacy Management System.
    Provides limited access to system features focused on inventory management.
    """
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        self.setWindowTitle("Pharmacy Management System - Pharmacist Dashboard")
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
        user_info = QLabel(f"Welcome, {self.user_data['fullname']} | Pharmacist")
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
        
        nav_inventory = QPushButton("Inventory")
        nav_inventory.setObjectName("navButton")
        nav_inventory.setCheckable(True)
        nav_inventory.clicked.connect(lambda: self.change_page(1))
        sidebar_layout.addWidget(nav_inventory)
        self.nav_buttons.append(nav_inventory)
        
        nav_dispense = QPushButton("Dispense Medication")
        nav_dispense.setObjectName("navButton")
        nav_dispense.setCheckable(True)
        nav_dispense.clicked.connect(lambda: self.change_page(2))
        sidebar_layout.addWidget(nav_dispense)
        self.nav_buttons.append(nav_dispense)
        
        nav_profile = QPushButton("My Profile")
        nav_profile.setObjectName("navButton")
        nav_profile.setCheckable(True)
        nav_profile.clicked.connect(lambda: self.change_page(3))
        sidebar_layout.addWidget(nav_profile)
        self.nav_buttons.append(nav_profile)
        
        # Main content
        self.main_content = QStackedWidget()
        self.main_content.setObjectName("mainContent")
        
        # Dashboard page
        dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_page)
        
        # Dashboard title
        dashboard_title = QLabel("Pharmacist Dashboard")
        dashboard_title.setFont(QFont("Arial", 20, QFont.Bold))
        dashboard_title.setContentsMargins(0, 0, 0, 20)
        
        # Dashboard cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Card 1: Total Medications
        card1 = QFrame()
        card1.setObjectName("dashboardCard")
        card1_layout = QVBoxLayout(card1)
        
        card1_title = QLabel("Total Medications")
        card1_title.setFont(QFont("Arial", 14))
        card1_value = QLabel("342")
        card1_value.setFont(QFont("Arial", 24, QFont.Bold))
        card1_value.setAlignment(Qt.AlignCenter)
        
        card1_layout.addWidget(card1_title)
        card1_layout.addWidget(card1_value)
        cards_layout.addWidget(card1)
        
        # Card 2: Low Stock Items
        card2 = QFrame()
        card2.setObjectName("dashboardCard")
        card2_layout = QVBoxLayout(card2)
        
        card2_title = QLabel("Low Stock Items")
        card2_title.setFont(QFont("Arial", 14))
        card2_value = QLabel("28")
        card2_value.setFont(QFont("Arial", 24, QFont.Bold))
        card2_value.setAlignment(Qt.AlignCenter)
        
        card2_layout.addWidget(card2_title)
        card2_layout.addWidget(card2_value)
        cards_layout.addWidget(card2)
        
        # Card 3: Out of Stock
        card3 = QFrame()
        card3.setObjectName("dashboardCard")
        card3_layout = QVBoxLayout(card3)
        
        card3_title = QLabel("Out of Stock")
        card3_title.setFont(QFont("Arial", 14))
        card3_value = QLabel("15")
        card3_value.setFont(QFont("Arial", 24, QFont.Bold))
        card3_value.setAlignment(Qt.AlignCenter)
        
        card3_layout.addWidget(card3_title)
        card3_layout.addWidget(card3_value)
        cards_layout.addWidget(card3)
        
        # Recent Activity
        activity_frame = QFrame()
        activity_frame.setObjectName("activityFrame")
        activity_layout = QVBoxLayout(activity_frame)
        
        activity_title = QLabel("Recent Activity")
        activity_title.setFont(QFont("Arial", 16, QFont.Bold))
        
        activity_table = QTableWidget(5, 3)
        activity_table.setHorizontalHeaderLabels(["Time", "Medication", "Activity"])
        activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Sample data
        activities = [
            ["10:30 AM", "Amoxicillin 500mg", "Updated stock: +50"],
            ["09:45 AM", "Paracetamol 500mg", "Dispensed: -20"],
            ["09:30 AM", "Ibuprofen 400mg", "Updated stock: +100"],
            ["Yesterday", "Metformin 850mg", "Noted low stock"],
            ["Yesterday", "Atorvastatin 20mg", "Dispensed: -30"]
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
        
        # Inventory page
        inventory_page = QWidget()
        inventory_layout = QVBoxLayout(inventory_page)
        
        # Inventory header
        inventory_header = QHBoxLayout()
        inventory_title = QLabel("Medication Inventory")
        inventory_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        # Search bar
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search medications...")
        search_box.setMinimumHeight(40)
        search_box.setMaximumWidth(300)
        search_box.textChanged.connect(lambda text: self.filter_medicines(text))
        
        inventory_header.addWidget(inventory_title)
        inventory_header.addStretch()
        inventory_header.addWidget(search_box)



        # Add search box to inventory header
        inventory_header.addWidget(search_box)
        inventory_header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        inventory_header.setContentsMargins(20, 0, 20, 0)
        inventory_header.setSpacing(20)
        



           
        # Inventory table
        self.inventory_table = QTableWidget()
        self.inventory_table.setObjectName("dataTable")
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Stock", "Status", "Actions"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.inventory_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.inventory_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        # Load inventory data
        self.load_inventory_data()
        
        # Add widgets to inventory layout
        inventory_layout.addLayout(inventory_header)
        inventory_layout.addWidget(self.inventory_table)
        
        # Dispense page
        dispense_page = QWidget()
        dispense_layout = QVBoxLayout(dispense_page)
        
        # Dispense title
        dispense_title = QLabel("Dispense Medication")
        dispense_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        # Dispense form container
        dispense_form_container = QFrame()
        dispense_form_container.setObjectName("formContainer")
        dispense_form_container.setMaximumWidth(600)
        dispense_form = QVBoxLayout(dispense_form_container)
        
        # Medication selection form
        medication_form = QFormLayout()
        medication_form.setVerticalSpacing(20)
        
        # Medication selector
        medication_combo = QComboBox()
        medication_combo.setMinimumHeight(40)
        medications = get_all_medications()
        for med in medications:
            if med['stock'] > 0:  # Only show medications in stock
                medication_combo.addItem(f"{med['name']} ({med['stock']} in stock)", med['id'])
        medication_form.addRow("Medication:", medication_combo)
        
        # Quantity
        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Enter quantity")
        quantity_input.setMinimumHeight(40)
        medication_form.addRow("Quantity:", quantity_input)
        
        # Patient name
        customer_input = QLineEdit()
        customer_input.setPlaceholderText("Enter customer name")
        customer_input.setMinimumHeight(40)
        medication_form.addRow("Patient Name:", customer_input)
        
        # Doctor name
        doctor_input = QLineEdit()
        doctor_input.setPlaceholderText("Enter doctor name")
        doctor_input.setMinimumHeight(40)
        medication_form.addRow("Prescribed By:", doctor_input)
        
        # Notes
        notes_input = QLineEdit()
        notes_input.setPlaceholderText("Any additional notes")
        notes_input.setMinimumHeight(40)
        medication_form.addRow("Notes:", notes_input)
        
        # Add form to container
        dispense_form.addLayout(medication_form)
        
        # Dispense button
        dispense_button = QPushButton("Dispense Medication")
        dispense_button.setObjectName("primaryButton")
        dispense_button.setMinimumHeight(50)
        dispense_button.setMaximumWidth(200)
        
        # Error label
        error_label = QLabel("")
        error_label.setObjectName("errorLabel")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setVisible(False)
        
        # Add widgets to dispense form
        dispense_form.addWidget(error_label)
        dispense_form.addWidget(dispense_button, alignment=Qt.AlignCenter)
        
        # Connect the dispense button
        dispense_button.clicked.connect(lambda: self.dispense_medication(
            medication_combo.currentData(),
            quantity_input.text(),
            customer_input.text(),
            doctor_input.text(),
            notes_input.text(),
            error_label
        ))
        
        # Add widgets to dispense layout
        dispense_layout.addWidget(dispense_title)
        dispense_layout.addWidget(dispense_form_container, alignment=Qt.AlignCenter)
        dispense_layout.addStretch()
        
        # Profile page
        profile_page = QWidget()
        profile_layout = QVBoxLayout(profile_page)
        
        # Profile title
        profile_title = QLabel("My Profile")
        profile_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        # Profile form container
        profile_form_container = QFrame()
        profile_form_container.setObjectName("formContainer")
        profile_form_container.setMaximumWidth(500)
        profile_form = QFormLayout(profile_form_container)
        profile_form.setVerticalSpacing(20)
        
        # Full name
        fullname_input = QLineEdit(self.user_data.get('fullname', ''))
        fullname_input.setMinimumHeight(40)
        profile_form.addRow("Full Name:", fullname_input)
        
        # Username (read-only)
        username_input = QLineEdit(self.user_data.get('username', ''))
        username_input.setMinimumHeight(40)
        username_input.setReadOnly(True)
        username_input.setStyleSheet("background-color: #f0f0f0;")
        profile_form.addRow("Username:", username_input)
        
        # Email
        email_input = QLineEdit(self.user_data.get('email', ''))
        email_input.setMinimumHeight(40)
        profile_form.addRow("Email:", email_input)
        
        # Phone
        phone_input = QLineEdit(self.user_data.get('phone', ''))
        phone_input.setMinimumHeight(40)
        profile_form.addRow("Phone:", phone_input)
        
        # Role (read-only)
        role_input = QLineEdit("Pharmacist")
        role_input.setMinimumHeight(40)
        role_input.setReadOnly(True)
        role_input.setStyleSheet("background-color: #f0f0f0;")
        profile_form.addRow("Role:", role_input)
        
        # Current password
        current_pass = QLineEdit()
        current_pass.setMinimumHeight(40)
        current_pass.setEchoMode(QLineEdit.Password)
        current_pass.setPlaceholderText("Enter current password to update")
        profile_form.addRow("Current Password:", current_pass)
        
        # New password
        new_pass = QLineEdit()
        new_pass.setMinimumHeight(40)
        new_pass.setEchoMode(QLineEdit.Password)
        new_pass.setPlaceholderText("Enter new password (leave blank to keep current)")
        profile_form.addRow("New Password:", new_pass)
        
        # Update profile button
        update_profile = QPushButton("Update Profile")
        update_profile.setObjectName("primaryButton")
        update_profile.setMinimumHeight(50)
        update_profile.setMaximumWidth(200)
        
        # Add widgets to profile layout
        profile_layout.addWidget(profile_title)
        profile_layout.addWidget(profile_form_container, alignment=Qt.AlignCenter)
        profile_layout.addWidget(update_profile, alignment=Qt.AlignCenter)
        profile_layout.addStretch()
        
        # Add pages to stacked widget
        self.main_content.addWidget(dashboard_page)
        self.main_content.addWidget(inventory_page)
        self.main_content.addWidget(dispense_page)
        self.main_content.addWidget(profile_page)
        
        # Add sidebar and main content to content area
        content_layout.addWidget(sidebar)
        content_layout.addWidget(self.main_content)
        
        # Add header and content area to main layout
        main_layout.addWidget(header)
        main_layout.addWidget(content_area)
        
        # Set central widget
        self.setCentralWidget(main_widget)
    

    def filter_medicines(self, text):
        for row in range(self.inventory_table.rowCount()):
            match = False
            for col in range(self.inventory_table.columnCount()):
                item = self.inventory_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.inventory_table.setRowHidden(row, not match)



    def update_dashboard_cards(self):
            try:
                conn = DatabaseConnection.get_connection()
                cursor = conn.cursor()

                # Total Medications
                cursor.execute("SELECT COUNT(*) FROM products")
                total = cursor.fetchone()[0]
                self.card1_value.setText(str(total))

                # Low Stock
                cursor.execute("SELECT COUNT(*) FROM products WHERE Quantity <= 10 AND Quantity > 0")
                low_stock = cursor.fetchone()[0]
                self.card2_value.setText(str(low_stock))

                # Out of Stock
                cursor.execute("SELECT COUNT(*) FROM products WHERE Quantity <= 0")
                out_stock = cursor.fetchone()[0]
                self.card3_value.setText(str(out_stock))

            except Exception as e:
                print("Dashboard stats error:", e)

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
    
    def load_inventory_data(self):
        """
        Load inventory data from the database
        """
        medications = get_all_medications()
        
        self.inventory_table.setRowCount(len(medications))
        
        for row, med in enumerate(medications):
            # ID
            id_item = QTableWidgetItem(str(med['id']))
            self.inventory_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(med['name'])
            self.inventory_table.setItem(row, 1, name_item)
            
            # Category
            category_item = QTableWidgetItem(med['category'])
            self.inventory_table.setItem(row, 2, category_item)
            
            # Stock
            stock_item = QTableWidgetItem(str(med['stock']))
            self.inventory_table.setItem(row, 3, stock_item)
            
            # Status
            status = "In Stock"
            status_color = QColor("#4CAF50")  # Green
            
            if med['stock'] <= 0:
                status = "Out of Stock"
                status_color = QColor("#F44336")  # Red
            elif med['stock'] <= 10:
                status = "Low Stock"
                status_color = QColor("#FFC107")  # Amber
                
            status_item = QTableWidgetItem(status)
            status_item.setForeground(status_color)
            self.inventory_table.setItem(row, 4, status_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(5)
            
            update_btn = QPushButton("Update Stock")
            update_btn.setObjectName("editButton")
            update_btn.setMaximumWidth(100)
            update_btn.clicked.connect(lambda _, med_id=med['id']: self.update_stock(med_id))
            
            actions_layout.addWidget(update_btn)
            
            self.inventory_table.setCellWidget(row, 5, actions_widget)
    
    def update_stock(self, med_id):
        """
        Show dialog to update medication stock
        """
        # Get medication data
        medication = get_medication_by_id(med_id)
        
        if not medication:
            QMessageBox.warning(self, "Error", "Medication not found.")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Update Stock: {medication['name']}")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet(StyleSheet.DIALOG_STYLE)
        
        layout = QVBoxLayout(dialog)
        
        # Form
        form = QFormLayout()
        
        # Current stock
        current_stock_label = QLabel(f"Current Stock: {medication['stock']}")
        current_stock_label.setFont(QFont("Arial", 12))
        form.addRow("", current_stock_label)
        
        # Stock change type
        stock_change_type = QComboBox()
        stock_change_type.addItems(["Add to Stock", "Remove from Stock"])
        stock_change_type.setMinimumHeight(40)
        form.addRow("Action:", stock_change_type)
        
        # Quantity
        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Enter quantity")
        quantity_input.setMinimumHeight(40)
        form.addRow("Quantity:", quantity_input)
        
        # Reason
        reason_input = QLineEdit()
        reason_input.setPlaceholderText("Reason for update")
        reason_input.setMinimumHeight(40)
        form.addRow("Reason:", reason_input)
        
        # Add form to layout
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        
        update_button = QPushButton("Update Stock")
        update_button.setObjectName("primaryButton")
        update_button.clicked.connect(lambda: self.save_stock_update(
            medication,
            stock_change_type.currentText(),
            quantity_input.text(),
            reason_input.text(),
            dialog
        ))
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(update_button)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_stock_update(self, medication, change_type, quantity_str, reason, dialog):
        """
        Save stock update to the database
        """
        # Validate input
        if not quantity_str or not reason:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all required fields.")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive number.")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return
        
        # Calculate new stock
        current_stock = medication['stock']
        if change_type == "Add to Stock":
            new_stock = current_stock + quantity
        else:  # Remove from Stock
            new_stock = current_stock - quantity
            if new_stock < 0:
                QMessageBox.warning(self, "Invalid Input", f"Cannot remove {quantity} items. Only {current_stock} available.")
                return
        
        # Update the stock
        update_medication_stock(medication['id'], new_stock, reason)
        
        # Reload inventory data
        self.load_inventory_data()
        
        # Close dialog
        dialog.accept()
    
    def dispense_medication(self, med_id, quantity_str, customer, doctor, notes, error_label):
        """
        Dispense medication to a customer
        """
        # Validate input
        if not med_id:
            self.show_error(error_label, "Please select a medication.")
            return
            
        if not quantity_str or not customer or not doctor:
            self.show_error(error_label, "Please fill in all required fields.")
            return
            
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive number.")
        except ValueError:
            self.show_error(error_label, "Quantity must be a valid positive number.")
            return
            
        # Get medication data
        medication = get_medication_by_id(med_id)
        
        if not medication:
            self.show_error(error_label, "Medication not found.")
            return
            
        # Check stock
        if quantity > medication['stock']:
            self.show_error(error_label, f"Not enough stock. Only {medication['stock']} available.")
            return
            
        # Update stock
        new_stock = medication['stock'] - quantity
        reason = f"Dispensed to customer: {customer}"
        if notes:
            reason += f" - {notes}"
            
        update_medication_stock(med_id, new_stock, reason)
        
        # Show success and reset
        QMessageBox.information(self, "Success", 
            f"Successfully dispensed {quantity} units of {medication['name']} to {customer}.")
            
        # Reset form fields (we'd need to modify the function parameters to include the form widgets)
        error_label.setVisible(False)
        
        # Reload inventory data
        self.load_inventory_data()
    
    def show_error(self, error_label, message):
        """
        Display error message
        """
        error_label.setText(message)
        error_label.setVisible(True)
    
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
        'id': 2,
        'username': 'pharmacist',
        'fullname': 'John Doe',
        'email': 'john@example.com',
        'phone': '123-456-7890',
        'role': 'pharmacist'
    }
    dashboard = PharmacistDashboard(user)
    dashboard.show()
    sys.exit(app.exec_())