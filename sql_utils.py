from sql_connection import DatabaseConnection

def insert_patient(patient_id, fname, lname, age, gender, phone, email, address):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        EXEC InsertPatient ?, ?, ?, ?, ?, ?, ?, ?
    """, (patient_id, fname, lname, age, gender, phone, email, address))
    conn.commit()

def insert_pharmacist(pharmacist_id, name, username, password, role):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        EXEC InsertPharmacist ?, ?, ?, ?, ?
    """, (pharmacist_id, name, username, password, role))
    conn.commit()

def authenticate_user(username, password):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Username, Role FROM users WHERE Username=? AND Password=?
    """, (username, password))
    return cursor.fetchone()


def login_pharmacist(username, password):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Pharmacist_ID, Role FROM pharmacists WHERE Username=? AND Password=?
    """, (username, password))
    return cursor.fetchone()

def insert_product(product_id, name, batch, expiry, quantity, price, reorder, manufacturer_id):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        EXEC InsertProduct ?, ?, ?, ?, ?, ?, ?, ?
    """, (product_id, name, batch, expiry, quantity, price, reorder, manufacturer_id))
    conn.commit()

def update_product_quantity(product_id, quantity):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        EXEC UpdateProductQuantity ?, ?
    """, (product_id, quantity))
    conn.commit()