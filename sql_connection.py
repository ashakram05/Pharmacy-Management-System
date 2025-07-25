import pyodbc

class DatabaseConnection:
    _connection = None

    @staticmethod
    def get_connection():
        if DatabaseConnection._connection is None:
            try:
                server = r'LAPTOP-7M5E1V4M'
                database = 'MediTracx'
                connection_string = (
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={server};DATABASE={database};Trusted_Connection=yes;'
                    f'Encrypt=yes;TrustServerCertificate=yes;'
                )
                DatabaseConnection._connection = pyodbc.connect(connection_string)
                print("✅ Connected to SQL Server successfully.")
            except pyodbc.Error as e:
                print("❌ Failed to connect to SQL Server:", e)
                raise
        return DatabaseConnection._connection