#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymssql
import os
import logging
from typing import Dict, List, Optional, Union, Tuple, Any
import hashlib
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("meditrack.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MediTracx")

class MediTracxDB:
    """
    Database connector class to interface with the MediTracx SQL Server database.
    Provides methods to execute stored procedures and queries.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MediTracxDB, cls).__new__(cls)
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance

    def connect(self, server="localhost", database="MediTracx", user="sa", password="YourPassword", as_dict=True):
        """
        Connect to the MS SQL Server database
        
        Args:
            server (str): SQL Server hostname or IP
            database (str): Database name
            user (str): SQL Server login username
            password (str): SQL Server login password
            as_dict (bool): Return rows as dictionaries instead of tuples
        """
        try:
            self.conn = pymssql.connect(
                server=server,
                user=user,
                password=password,
                database=database,
                as_dict=as_dict
            )
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database {database} on {server}")
            return True
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            return False

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            logger.info("Database connection closed")

    def commit(self):
        """Commit changes to the database"""
        if self.conn:
            self.conn.commit()

    def execute_stored_procedure(self, procedure_name: str, params: tuple = None) -> Optional[List[Dict]]:
        """
        Execute a stored procedure
        
        Args:
            procedure_name (str): Name of the stored procedure
            params (tuple): Parameters for the stored procedure
            
        Returns:
            Optional[List[Dict]]: Results as a list of dictionaries, or None on error
        """
        if not self.conn:
            logger.error("No database connection")
            return None
        
        try:
            if params:
                self.cursor.callproc(procedure_name, params)
            else:
                self.cursor.callproc(procedure_name)
            
            # Fetch results if any
            results = []
            for result_set in self.cursor.stored_results():
                results.extend(result_set.fetchall())
            return results
        except Exception as e:
            logger.error(f"Error executing stored procedure {procedure_name}: {str(e)}")
            return None

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """
        Execute an SQL query
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            
        Returns:
            Optional[List[Dict]]: Results as a list of dictionaries, or None on error
        """
        if not self.conn:
            logger.error("No database connection")
            return None
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return None
    
    # ========================
    # Patient Management
    # ========================
    def get_all_patients(self) -> Optional[List[Dict]]:
        """Get all patients from the database"""
        return self.execute_query("SELECT * FROM patients ORDER BY FName, LName")
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Dict]:
        """Get a patient by ID"""
        result = self.execute_query("SELECT * FROM patients WHERE Patient_ID = %s", (patient_id,))
        return result[0] if result else None
    
    def insert_patient(self, patient_id: str, fname: str, lname: str, 
                       age: int, gender: str, phone: str = None, 
                       email: str = None, address: str = None) -> bool:
        """Insert a new patient using stored procedure"""
        try:
            params = (patient_id, fname, lname, age, gender, phone, email, address)
            self.execute_stored_procedure("InsertPatient", params)
            self.commit()
            logger.info(f"Patient {patient_id} added successfully")
            return True
        except Exception as e:
            logger.error(f"Error inserting patient: {str(e)}")
            return False
    
    def update_patient_email(self, patient_id: str, email: str) -> bool:
        """Update a patient's email using stored procedure"""
        try:
            self.execute_stored_procedure("UpdatePatientEmail", (patient_id, email))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating patient email: {str(e)}")
            return False
    
    def delete_patient(self, patient_id: str) -> bool:
        """Delete a patient using stored procedure"""
        try:
            self.execute_stored_procedure("DeletePatient", (patient_id,))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting patient: {str(e)}")
            return False

    # ========================
    # Pharmacist Management
    # ========================
    def get_all_pharmacists(self) -> Optional[List[Dict]]:
        """Get all pharmacists from the database"""
        return self.execute_query("SELECT * FROM pharmacists ORDER BY Name")
    
    def get_pharmacist_by_id(self, pharmacist_id: str) -> Optional[Dict]:
        """Get a pharmacist by ID"""
        result = self.execute_query("SELECT * FROM pharmacists WHERE Pharmacist_ID = %s", (pharmacist_id,))
        return result[0] if result else None
    
    def get_pharmacist_by_username(self, username: str) -> Optional[Dict]:
        """Get a pharmacist by username"""
        result = self.execute_query("SELECT * FROM pharmacists WHERE Username = %s", (username,))
        return result[0] if result else None
    
    def authenticate_pharmacist(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate a pharmacist by username and password
        
        Returns:
            Dict: Pharmacist data if authentication is successful, None otherwise
        """
        # Hash password for security (in production, use more secure method)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        result = self.execute_query(
            "SELECT * FROM pharmacists WHERE Username = %s AND Password = %s", 
            (username, hashed_password)
        )
        
        if result:
            pharmacist = result[0]
            # Get role-specific information
            if pharmacist['Role'] == 'admin':
                admin_info = self.execute_query(
                    "SELECT * FROM admin_pharmacist WHERE Pharmacist_ID = %s", 
                    (pharmacist['Pharmacist_ID'],)
                )
                if admin_info:
                    pharmacist['Access_Level'] = admin_info[0]['Access_Level']
            elif pharmacist['Role'] == 'staff':
                staff_info = self.execute_query(
                    "SELECT * FROM staff_pharmacist WHERE Pharmacist_ID = %s", 
                    (pharmacist['Pharmacist_ID'],)
                )
                if staff_info:
                    pharmacist['Shift'] = staff_info[0]['Shift']
                    
            return pharmacist
        
        return None
    
    def insert_pharmacist(self, pharmacist_id: str, name: str, username: str, 
                         password: str, role: str) -> bool:
        """Insert a new pharmacist using stored procedure"""
        try:
            # Hash password for security
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            params = (pharmacist_id, name, username, hashed_password, role)
            self.execute_stored_procedure("InsertPharmacist", params)
            self.commit()
            logger.info(f"Pharmacist {pharmacist_id} added successfully")
            return True
        except Exception as e:
            logger.error(f"Error inserting pharmacist: {str(e)}")
            return False
    
    def update_pharmacist_password(self, pharmacist_id: str, password: str) -> bool:
        """Update a pharmacist's password using stored procedure"""
        try:
            # Hash password for security
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            self.execute_stored_procedure("UpdatePharmacistPassword", (pharmacist_id, hashed_password))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating pharmacist password: {str(e)}")
            return False
    
    def delete_pharmacist(self, pharmacist_id: str) -> bool:
        """Delete a pharmacist using stored procedure"""
        try:
            self.execute_stored_procedure("DeletePharmacist", (pharmacist_id,))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting pharmacist: {str(e)}")
            return False
    
    # ========================
    # Product Management
    # ========================
    def get_all_products(self) -> Optional[List[Dict]]:
        """Get all products from the database"""
        return self.execute_query("SELECT * FROM products ORDER BY Name")
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Get a product by ID"""
        result = self.execute_query("SELECT * FROM products WHERE Product_ID = %s", (product_id,))
        return result[0] if result else None
    
    def get_products_by_manufacturer(self, manufacturer_id: str) -> Optional[List[Dict]]:
        """Get products by manufacturer ID"""
        return self.execute_query("SELECT * FROM products WHERE Manufacturer_ID = %s ORDER BY Name", (manufacturer_id,))
    
    def get_products_below_reorder_level(self) -> Optional[List[Dict]]:
        """Get products that are below their reorder level"""
        return self.execute_query("SELECT * FROM products WHERE Quantity <= Reorder_Level ORDER BY Name")
    
    def get_products_expiring_soon(self, days: int = 90) -> Optional[List[Dict]]:
        """Get products that are expiring within the specified number of days"""
        query = """
            SELECT * FROM products 
            WHERE DATEDIFF(day, GETDATE(), Expiry_Date) <= %s
            ORDER BY Expiry_Date
        """
        return self.execute_query(query, (days,))
    
    def insert_product(self, product_id: str, name: str, batch_no: str, expiry_date: str,
                      quantity: int, unit_price: float, reorder_level: int, 
                      manufacturer_id: str) -> bool:
        """Insert a new product using stored procedure"""
        try:
            params = (product_id, name, batch_no, expiry_date, quantity, 
                     unit_price, reorder_level, manufacturer_id)
            self.execute_stored_procedure("InsertProduct", params)
            self.commit()
            logger.info(f"Product {product_id} added successfully")
            return True
        except Exception as e:
            logger.error(f"Error inserting product: {str(e)}")
            return False
    
    def update_product_quantity(self, product_id: str, quantity: int) -> bool:
        """Update a product's quantity using stored procedure"""
        try:
            self.execute_stored_procedure("UpdateProductQuantity", (product_id, quantity))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating product quantity: {str(e)}")
            return False
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product using stored procedure"""
        try:
            self.execute_stored_procedure("DeleteProduct", (product_id,))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            return False
    
    # ========================
    # Sale Management
    # ========================
    def get_all_sales(self) -> Optional[List[Dict]]:
        """Get all sales from the database"""
        return self.execute_query("SELECT * FROM sales ORDER BY Sale_Date DESC")
    
    def get_sale_by_id(self, sale_id: str) -> Optional[Dict]:
        """Get a sale by ID with its items"""
        sale = self.execute_query("SELECT * FROM sales WHERE Sale_ID = %s", (sale_id,))
        if not sale:
            return None
        
        sale_info = sale[0]
        sale_items = self.execute_query("""
            SELECT si.*, p.Name, p.Unit_Price 
            FROM sale_items si
            JOIN products p ON si.Product_ID = p.Product_ID
            WHERE si.Sale_ID = %s
        """, (sale_id,))
        
        sale_info['items'] = sale_items
        
        # Add payment information if available
        cash_payment = self.execute_query("SELECT * FROM cash_sales WHERE Sale_ID = %s", (sale_id,))
        credit_payment = self.execute_query("SELECT * FROM credit_sales WHERE Sale_ID = %s", (sale_id,))
        
        if cash_payment:
            sale_info['payment'] = cash_payment[0]
            sale_info['payment_type'] = 'cash'
        elif credit_payment:
            sale_info['payment'] = credit_payment[0]
            sale_info['payment_type'] = 'credit'
        
        return sale_info
    
    def get_sales_by_patient(self, patient_id: str) -> Optional[List[Dict]]:
        """Get sales by patient ID"""
        return self.execute_query("SELECT * FROM sales WHERE Patient_ID = %s ORDER BY Sale_Date DESC", (patient_id,))
    
    def get_sales_by_date_range(self, start_date: str, end_date: str) -> Optional[List[Dict]]:
        """Get sales within a date range"""
        query = """
            SELECT * FROM sales 
            WHERE Sale_Date BETWEEN %s AND %s
            ORDER BY Sale_Date DESC
        """
        return self.execute_query(query, (start_date, end_date))
    
    def insert_sale(self, sale_id: str, patient_id: str, total_amount: float,
                   sale_date: str, status: str, pharmacist_id: str) -> bool:
        """Insert a new sale using stored procedure"""
        try:
            params = (sale_id, patient_id, total_amount, sale_date, status, pharmacist_id)
            self.execute_stored_procedure("InsertSale", params)
            self.commit()
            logger.info(f"Sale {sale_id} added successfully")
            return True
        except Exception as e:
            logger.error(f"Error inserting sale: {str(e)}")
            return False
    
    def insert_sale_item(self, sale_id: str, product_id: str, quantity: int, subtotal: float) -> bool:
        """Insert a new sale item using stored procedure"""
        try:
            params = (sale_id, product_id, quantity, subtotal)
            self.execute_stored_procedure("InsertSaleItem", params)
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error inserting sale item: {str(e)}")
            return False
    
    def update_sale_status(self, sale_id: str, status: str) -> bool:
        """Update a sale's status using stored procedure"""
        try:
            self.execute_stored_procedure("UpdateSaleStatus", (sale_id, status))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating sale status: {str(e)}")
            return False
    
    def delete_sale(self, sale_id: str) -> bool:
        """Delete a sale using stored procedure"""
        try:
            # Delete related records from sale_items
            self.execute_query("DELETE FROM sale_items WHERE Sale_ID = %s", (sale_id,))
            
            # Delete from payment tables
            self.execute_query("DELETE FROM cash_sales WHERE Sale_ID = %s", (sale_id,))
            self.execute_query("DELETE FROM credit_sales WHERE Sale_ID = %s", (sale_id,))
            
            # Delete the sale
            self.execute_stored_procedure("DeleteSale", (sale_id,))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting sale: {str(e)}")
            return False
    
    # ========================
    # Prescription Management
    # ========================
    def get_all_prescriptions(self) -> Optional[List[Dict]]:
        """Get all prescriptions from the database"""
        return self.execute_query("""
            SELECT p.*, pt.FName + ' ' + pt.LName AS PatientName, ph.Name AS PharmacistName
            FROM prescriptions p
            JOIN patients pt ON p.Patient_ID = pt.Patient_ID
            JOIN pharmacists ph ON p.Pharmacist_ID = ph.Pharmacist_ID
            ORDER BY p.Date_Issued DESC
        """)
    
    def get_prescription_by_id(self, prescription_id: str) -> Optional[Dict]:
        """Get a prescription by ID with its details"""
        prescription = self.execute_query("""
            SELECT p.*, pt.FName + ' ' + pt.LName AS PatientName, ph.Name AS PharmacistName
            FROM prescriptions p
            JOIN patients pt ON p.Patient_ID = pt.Patient_ID
            JOIN pharmacists ph ON p.Pharmacist_ID = ph.Pharmacist_ID
            WHERE p.Prescription_ID = %s
        """, (prescription_id,))
        
        if not prescription:
            return None
        
        prescription_info = prescription[0]
        details = self.execute_query("""
            SELECT pd.*, pr.Name AS ProductName
            FROM prescription_details pd
            JOIN products pr ON pd.Product_ID = pr.Product_ID
            WHERE pd.Prescription_ID = %s
        """, (prescription_id,))
        
        prescription_info['details'] = details
        return prescription_info
    
    def get_prescriptions_by_patient(self, patient_id: str) -> Optional[List[Dict]]:
        """Get prescriptions by patient ID"""
        return self.execute_query("""
            SELECT p.*, ph.Name AS PharmacistName
            FROM prescriptions p
            JOIN pharmacists ph ON p.Pharmacist_ID = ph.Pharmacist_ID
            WHERE p.Patient_ID = %s
            ORDER BY p.Date_Issued DESC
        """, (patient_id,))
    
    def insert_prescription(self, prescription_id: str, patient_id: str, 
                           pharmacist_id: str, date_issued: str) -> bool:
        """Insert a new prescription"""
        try:
            query = """
                INSERT INTO prescriptions (Prescription_ID, Patient_ID, Pharmacist_ID, Date_Issued)
                VALUES (%s, %s, %s, %s)
            """
            self.execute_query(query, (prescription_id, patient_id, pharmacist_id, date_issued))
            self.commit()
            logger.info(f"Prescription {prescription_id} added successfully")
            return True
        except Exception as e:
            logger.error(f"Error inserting prescription: {str(e)}")
            return False
    
    def insert_prescription_detail(self, prescription_id: str, product_id: str,
                                  dosage: str, duration: str) -> bool:
        """Insert a new prescription detail"""
        try:
            query = """
                INSERT INTO prescription_details (Prescription_ID, Product_ID, Dosage, Duration)
                VALUES (%s, %s, %s, %s)
            """
            self.execute_query(query, (prescription_id, product_id, dosage, duration))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error inserting prescription detail: {str(e)}")
            return False
    
    # ========================
    # Data Analytics
    # ========================
    def get_sales_summary_by_date(self) -> Optional[List[Dict]]:
        """Get sales summary by date using the view"""
        return self.execute_query("SELECT * FROM vw_SalesSummaryByDate ORDER BY Sale_Date DESC")
    
    def get_product_stock_status(self) -> Optional[List[Dict]]:
        """Get product stock status using the view"""
        return self.execute_query("SELECT * FROM vw_ProductStockStatus ORDER BY Name")
    
    def get_patient_full_info(self) -> Optional[List[Dict]]:
        """Get patient information with prescription count using the view"""
        return self.execute_query("SELECT * FROM vw_PatientFullInfo ORDER BY LName, FName")
    
    def get_sales_by_month(self, year: int) -> Optional[List[Dict]]:
        """Get monthly sales summary for a specific year"""
        query = """
            SELECT 
                MONTH(Sale_Date) AS Month,
                COUNT(Sale_ID) AS TotalSales,
                SUM(Total_Amount) AS TotalRevenue
            FROM sales
            WHERE YEAR(Sale_Date) = %s
            GROUP BY MONTH(Sale_Date)
            ORDER BY Month
        """
        return self.execute_query(query, (year,))
    
    def get_top_selling_products(self, limit: int = 10) -> Optional[List[Dict]]:
        """Get top selling products"""
        query = """
            SELECT 
                p.Product_ID,
                p.Name,
                SUM(si.Quantity) AS TotalQuantitySold,
                SUM(si.Subtotal) AS TotalRevenue
            FROM sale_items si
            JOIN products p ON si.Product_ID = p.Product_ID
            JOIN sales s ON si.Sale_ID = s.Sale_ID
            GROUP BY p.Product_ID, p.Name
            ORDER BY TotalQuantitySold DESC
            OFFSET 0 ROWS
            FETCH NEXT %s ROWS ONLY
        """
        return self.execute_query(query, (limit,))
    
    def get_expiring_products_report(self) -> Optional[List[Dict]]:
        """Get a report of products expiring in the next 90 days"""
        query = """
            SELECT 
                p.Product_ID,
                p.Name,
                p.Batch_No,
                p.Quantity,
                p.Expiry_Date,
                DATEDIFF(day, GETDATE(), p.Expiry_Date) AS DaysUntilExpiry,
                m.Name AS Manufacturer
            FROM products p
            JOIN manufacturers m ON p.Manufacturer_ID = m.Manufacturer_ID
            WHERE DATEDIFF(day, GETDATE(), p.Expiry_Date) BETWEEN 0 AND 90
            AND p.Quantity > 0
            ORDER BY DaysUntilExpiry
        """
        return self.execute_query(query)


# Initialize database connection
def init_db(server="localhost", database="MediTracx", user="sa", password="YourPassword"):
    """Initialize database connection with custom connection parameters"""
    db = MediTracxDB()
    return db.connect(server, database, user, password)


# Testing the connection
if __name__ == "__main__":
    db = MediTracxDB()
    if db.connect():
        print("Database connection successful!")
        # Test a simple query
        patients = db.get_all_patients()
        if patients:
            print(f"Found {len(patients)} patients")
        else:
            print("No patients found or error occurred")
        db.close()
    else:
        print("Database connection failed!")