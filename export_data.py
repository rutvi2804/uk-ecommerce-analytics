import pandas as pd
from sqlalchemy import create_engine
import urllib
import os

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=uk_ecommerce;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
encoded = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded}")

os.makedirs('data/exports', exist_ok=True)

tables = {
    'fct_sales':         'SELECT * FROM dbo.fct_sales',
    'fct_rfm_segments':  'SELECT * FROM dbo.fct_rfm_segments',
    'fct_cohort':        'SELECT * FROM dbo.fct_cohort',
    'fct_country_sales': 'SELECT * FROM dbo.fct_country_sales',
    'stg_transactions':  '''
        SELECT description, total_price, quantity, invoice_no
        FROM dbo.stg_transactions
    '''
}

for name, query in tables.items():
    print(f"Exporting {name}...")
    df = pd.read_sql(query, engine)
    df.to_csv(f'data/exports/{name}.csv', index=False)
    print(f"Saved {len(df):,} rows to data/exports/{name}.csv")

print("\nAll exports complete!")