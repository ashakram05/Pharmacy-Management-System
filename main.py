#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow
from database import init_database

def main():
    """
    Entry point for the Pharmacy Management System application.
    Creates the application and shows the login window.
    """
    # Initialize database
    init_database()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Execute application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()