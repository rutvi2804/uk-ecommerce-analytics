import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine,text
import urllib
import time

#Configuration

SERVER = 'rutvi'
INSTANCE = 'SQLEXPRESS'
DATABASE = 'uk_ecommerce'
CSV_PATH = 'data/raw/ecommerce.csv'
TABLE_NAME = 'raw_transactions'
USERNAME = 'rutvi'
PASSWORD = 'Rutvi@1234'
SCHEMA = 'dbo'

#Create database connection
print("Connecting to SQL Server")

#Direct connection string format 
import urllib

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER}\\{INSTANCE};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
    f"Encrypt=yes;"
)

encoded = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded}")

#Test connection
try:    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        version = result.fetchone()[0]
        print(f"Connected successfully!")
        print(f"SQL Server Version : {version[:50]}")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

#Read CSV file
print("\n Reading CSV file...")
start = time.time()

df = pd.read_csv(CSV_PATH,encoding='unicode_escape',
        dtype={        
        'InvoiceNo': str,
        'StockCode': str,
        'Description': str,
        'CustomerID': str,
        'Country': str})

end = time.time()
print(f"csv loaded in {round(end-start,2)} seconds")
print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

#Basic Inspection
print("\n columns info")
print(df.dtypes)

print("\n Null counts")
print(df.isnull().sum())

print("\n Sample rows")
print(df.head(3))

#Prepration before oading
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

#Strip whitespace from string columns
df['Description'] = df['Description'].str.strip()
df['Country'] = df['Country'].str.strip()
df['InvoiceNo'] = df['InvoiceNo'].str.strip()
df['StockCode'] = df['StockCode'].str.strip()

#Rename the columns
df.columns = [
    'invoice_no',
    'stock_code',
    'description',
    'quantity',
    'invoice_date',
    'unit_price',
    'customer_id',
    'country'
]
print(f"Columns renamed to snake_case")
print(f"InvoiceDate converted to datetime")

#Load into SQL SERVER
print(f"\nLoading {df.shape[0]:,} rows into SQL Server")
print("This will take 2-5 minutes")

start = time.time()

df.to_sql(
    name= TABLE_NAME,
    con=engine,
    schema= SCHEMA,
    if_exists='replace',
    index= False,
    chunksize=100
)
end=time.time()
print(f"Data loaded in {round(end - start, 2)} seconds")

#Verify the Load
print("\n Verifying data in SQL Server...")

with engine.connect() as conn:

    #Row count
    result = conn.execute(text(f"SELECT COUNT(*) FROM {SCHEMA}.{TABLE_NAME}"))
    count = result.fetchone()[0]
    print(f"Rows in SQL Server : {count:,}")

    #sample rows
    result = conn.execute(text(f"SELECT TOP 5 * FROM {SCHEMA}.{TABLE_NAME}"))
    rows = result.fetchall()
    for row in rows:
        print(row)

    # Null check on key columns
    result = conn.execute(text(f"""
        SELECT
            SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customers,
            SUM(CASE WHEN invoice_no IS NULL THEN 1 ELSE 0 END) AS null_invoices,
            SUM(CASE WHEN unit_price IS NULL THEN 1 ELSE 0 END) AS null_prices
        FROM {SCHEMA}.{TABLE_NAME}
    """))
    nulls = result.fetchone()
    print(f"\nNull customer_ids: {nulls[0]:,}")
    print(f"Null invoice_nos: {nulls[1]:,}")
    print(f"Null unit_prices: {nulls[2]:,}")

print(f"Table: {SCHEMA}.{TABLE_NAME}")
print(f"Database: {DATABASE}")