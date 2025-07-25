#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StyleSheet:
    """
    Centralized style definitions for the Pharmacy Management System GUI
    Uses QSS (Qt Style Sheets) which is similar to CSS
    """
    
    # Main application style
    MAIN_STYLE = """
        /* Global styles */
        QMainWindow, QDialog {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        
        /* Header styles */
        #header {
            background-color: #2c3e50;
            color: white;
            min-height: 60px;
            border: none;
        }
        
        #header QLabel {
            color: white;
        }
        
        #logoutButton {
            background-color: transparent;
            border: 1px solid #e74c3c;
            border-radius: 4px;
            color: #e74c3c;
            padding: 5px 10px;
            font-weight: bold;
        }
        
        #logoutButton:hover {
            background-color: #e74c3c;
            color: white;
        }
        
        /* Sidebar styles */
        #sidebar {
            background-color: #34495e;
            min-width: 200px;
            padding: 20px 0px;
            border: none;
        }
        
        #navButton {
            text-align: left;
            padding: 12px 15px;
            border: none;
            border-left: 5px solid transparent;
            border-radius: 0px;
            background-color: transparent;
            color: #ecf0f1;
            font-size: 14px;
            font-weight: 500;
        }
        
        #navButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        #navButton:checked {
            background-color: rgba(52, 152, 219, 0.2);
            border-left: 5px solid #3498db;
            font-weight: bold;
        }
        
        /* Main content styles */
        #mainContent {
            background-color: #f5f5f5;
            border: none;
            padding: 20px;
        }
        
        /* Login and registration panels */
        #leftPanel {
            background-color: #2c3e50;
            padding: 30px;
        }
        
        #rightPanel {
            background-color: #f5f5f5;
            padding: 30px;
        }
        
        #formContainer {
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Form elements */
        QLineEdit, QComboBox {
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
            selection-background-color: #3498db;
        }
        
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #3498db;
        }
        
        /* Button styles */
        QPushButton {
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 8px 16px;
            color: #2c3e50;
        }
        
        QPushButton:hover {
            background-color: #dcdcdc;
        }
        
        QPushButton:pressed {
            background-color: #bdc3c7;
        }
        
        #primaryButton {
            background-color: #3498db;
            border: none;
            color: white;
            font-weight: bold;
        }
        
        #primaryButton:hover {
            background-color: #2980b9;
        }
        
        #primaryButton:pressed {
            background-color: #1a5276;
        }
        
        #linkButton {
            background-color: transparent;
            border: none;
            color: #3498db;
            text-decoration: none;
            padding: 0px;
        }
        
        #linkButton:hover {
            color: #2980b9;
            text-decoration: underline;
        }
    """
    
    # Additional styles for dashboard
    DASHBOARD_STYLE = """
        /* Dashboard cards */
        #dashboardCard {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Dashboard activity frame */
        #activityFrame, #settingsFrame {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Table styles */
        QTableWidget {
            border: none;
            background-color: white;
            gridline-color: #f0f0f0;
            border-radius: 8px;
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QTableWidget::item:selected {
            background-color: #e3f2fd;
            color: #2c3e50;
        }
        
        QHeaderView::section {
            background-color: #f5f5f5;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        
        #dataTable {
            margin: 10px;
        }
        
        /* Tab widget styles */
        #contentTabs {
            background-color: white;
            border: none;
        }
        
        #contentTabs::pane {
            border: none;
            background-color: white;
            border-radius: 8px;
            padding: 10px;
        }
        
        QTabBar::tab {
            background-color: #f5f5f5;
            border: none;
            padding: 10px 15px;
            margin-right: 5px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        
        QTabBar::tab:!selected {
            margin-top: 2px;
        }
        
        /* Action buttons in tables */
        #editButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 8px;
            font-size: 11px;
        }
        
        #editButton:hover {
            background-color: #2980b9;
        }
        
        #deleteButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 8px;
            font-size: 11px;
        }
        
        #deleteButton:hover {
            background-color: #c0392b;
        }
        
        /* Error label */
        #errorLabel {
            color: #e74c3c;
            font-weight: bold;
            padding: 5px;
            background-color: #fadbd8;
            border-radius: 4px;
        }
    """
    
    # Dialog styles
    DIALOG_STYLE = """
        QDialog {
            background-color: #f5f5f5;
        }
        
        QDialog QLabel {
            color: #2c3e50;
        }
        
        QDialog #formContainer {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
        }
    """