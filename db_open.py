import pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=GREEN;'
    'DATABASE=Proiect;'                
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()