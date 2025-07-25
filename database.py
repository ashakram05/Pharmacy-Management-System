#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import hashlib
import datetime
from typing import Dict, List, Optional, Union, Tuple

class Database:
    """
    Singleton database class to manage database connections and operations
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance
    
    def connect(self):
        """
        Connect to the SQLite database
        """
        if self.conn is None:
            # Create database directory if it doesn't exist
            db_dir = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(db_dir, exist_ok=True)
            
            # Connect to database
            db_path = os.path.join(db_dir, 'pharmacy.db')
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
    
    def close(self):
        """
        Close the database connection
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def commit(self):
        """
        Commit changes to the database
        """
        if self.conn:
            self.conn.commit()

# Create database tables
def init_database():
    """
    Initialize the database and create tables if they don't exist
    """
    db = Database()
    db.connect()
    
    # Create users table
    db.cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        role TEXT NOT NULL,
        active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create medications table
    db.cursor.execute('''
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        stock INTEGER DEFAULT 0,
        price REAL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create stock_history table
    db.cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication_id INTEGER,
        previous_stock INTEGER,
        new_stock INTEGER,
        changed_by INTEGER,
        reason TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medication_id) REFERENCES medications(id),
        FOREIGN KEY (changed_by) REFERENCES users(id)
    )
    ''')
    
    # Create admin user if none exists
    db.cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('admin',))
    if db.cursor.fetchone()[0] == 0:
        # Create default admin user
        password_hash = hash_password('admin123')
        db.cursor.execute(
            'INSERT INTO users (username, password, fullname, email, phone, role) VALUES (?, ?, ?, ?, ?, ?)',
            ('admin', password_hash, 'System Administrator', 'admin@pharmacy.com', '123-456-7890', 'admin')
        )
    
    # Add some sample medications if none exist
    db.cursor.execute('SELECT COUNT(*) FROM medications')
    if db.cursor.fetchone()[0] == 0:
        sample_medications = [
            ('Amoxicillin 500mg', 'Antibiotic capsules', 'Antibiotics', 100, 12.99),
            ('Paracetamol 500mg', 'Pain reliever tablets', 'Analgesics', 200, 5.99),
            ('Ibuprofen 400mg', 'Anti-inflammatory tablets', 'Analgesics', 150, 6.99),
            ('Metformin 850mg', 'Anti-diabetic tablets', 'Diabetic', 80, 15.99),
            ('Atorvastatin 20mg', 'Cholesterol lowering tablets', 'Cardiovascular', 120, 22.99),
            ('Cetirizine 10mg', 'Antihistamine tablets', 'Allergy', 90, 9.99),
            ('Omeprazole 20mg', 'Proton pump inhibitor', 'Gastrointestinal', 70, 14.99),
            ('Amlodipine 5mg', 'Calcium channel blocker', 'Cardiovascular', 100, 18.99)
        ]
        
        for med in sample_medications:
            db.cursor.execute(
                'INSERT INTO medications (name, description, category, stock, price) VALUES (?, ?, ?, ?, ?)',
                med
            )
    
    # Commit changes
    db.commit()

def hash_password(password: str) -> str:
    """
    Hash a password for secure storage
    """
    # Use SHA-256 for password hashing (in a production app, use a more secure method like bcrypt)
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(hashed_password: str, input_password: str) -> bool:
    """
    Verify that an input password matches the stored hash
    """
    return hashed_password == hash_password(input_password)

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user by username and password
    
    Returns:
        Dict: User data if authentication is successful, None otherwise
    """
    db = Database()
    db.connect()
    
    db.cursor.execute('SELECT * FROM users WHERE username = ? AND active = 1', (username,))
    user = db.cursor.fetchone()
    
    if user and verify_password(user['password'], password):
        # Convert user row to dictionary
        user_dict = dict(user)
        # Remove password from returned data for security
        user_dict.pop('password', None)
        return user_dict
    
    return None

def filter_medicines(self, text):
    for row in range(self.table_inventory.rowCount()):
        match = False
        for col in range(self.table_inventory.columnCount()):
            item = self.table_inventory.item(row, col)
            if item and text.lower() in item.text().lower():
                match = True
                break
        self.table_inventory.setRowHidden(row, not match)


def username_exists(username: str) -> bool:
    """
    Check if a username already exists in the database
    """
    db = Database()
    db.connect()
    
    db.cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
    count = db.cursor.fetchone()[0]
    
    return count > 0

def register_user(username: str, password: str, fullname: str, email: str, phone: str, role: str) -> bool:
    """
    Register a new user in the database
    
    Returns:
        bool: True if registration is successful, False otherwise
    """
    db = Database()
    db.connect()
    
    try:
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert the new user
        db.cursor.execute(
            'INSERT INTO users (username, password, fullname, email, phone, role) VALUES (?, ?, ?, ?, ?, ?)',
            (username, password_hash, fullname, email, phone, role)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False

def get_all_users() -> List[Dict]:
    """
    Get all users from the database
    
    Returns:
        List[Dict]: List of user dictionaries
    """
    db = Database()
    db.connect()
    
    db.cursor.execute('SELECT id, username, fullname, email, phone, role, active FROM users')
    users = [dict(row) for row in db.cursor.fetchall()]
    
    return users

def get_all_medications() -> List[Dict]:
    """
    Get all medications from the database
    
    Returns:
        List[Dict]: List of medication dictionaries
    """
    db = Database()
    db.connect()
    
    db.cursor.execute('SELECT * FROM medications')
    medications = [dict(row) for row in db.cursor.fetchall()]
    
    return medications

def get_medication_by_id(medication_id: int) -> Optional[Dict]:
    """
    Get a medication by ID
    
    Args:
        medication_id (int): ID of the medication to retrieve
    
    Returns:
        Dict: Medication data if found, None otherwise
    """
    db = Database()
    db.connect()
    
    db.cursor.execute('SELECT * FROM medications WHERE id = ?', (medication_id,))
    medication = db.cursor.fetchone()
    
    return dict(medication) if medication else None

def add_medication(name: str, description: str, category: str, stock: int, price: float) -> bool:
    """
    Add a new medication to the database
    
    Returns:
        bool: True if operation is successful, False otherwise
    """
    db = Database()
    db.connect()
    
    try:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db.cursor.execute(
            'INSERT INTO medications (name, description, category, stock, price, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, description, category, stock, price, now, now)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False

def update_medication_stock(medication_id: int, new_stock: int, reason: str, user_id: int = None) -> bool:
    """
    Update medication stock and record the change in stock_history
    
    Args:
        medication_id (int): ID of the medication to update
        new_stock (int): New stock quantity
        reason (str): Reason for the stock change
        user_id (int, optional): ID of the user making the change
    
    Returns:
        bool: True if operation is successful, False otherwise
    """
    db = Database()
    db.connect()
    
    try:
        # Get current stock
        db.cursor.execute('SELECT stock FROM medications WHERE id = ?', (medication_id,))
        result = db.cursor.fetchone()
        
        if not result:
            return False
            
        previous_stock = result['stock']
        
        # Update medication stock
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.cursor.execute(
            'UPDATE medications SET stock = ?, updated_at = ? WHERE id = ?',
            (new_stock, now, medication_id)
        )
        
        # Record in stock_history
        db.cursor.execute(
            'INSERT INTO stock_history (medication_id, previous_stock, new_stock, changed_by, reason) VALUES (?, ?, ?, ?, ?)',
            (medication_id, previous_stock, new_stock, user_id, reason)
        )
        
        db.commit()
        return True
    except sqlite3.Error:
        return False

def delete_medication(medication_id: int) -> bool:
    """
    Delete a medication from the database
    
    Args:
        medication_id (int): ID of the medication to delete
    
    Returns:
        bool: True if operation is successful, False otherwise
    """
    db = Database()
    db.connect()
    
    try:
        # Delete medication
        db.cursor.execute('DELETE FROM medications WHERE id = ?', (medication_id,))
        
        # Delete related stock history
        db.cursor.execute('DELETE FROM stock_history WHERE medication_id = ?', (medication_id,))
        
        db.commit()
        return True
    except sqlite3.Error:
        return False