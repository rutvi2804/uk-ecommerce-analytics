import pandas as pd
from sqlalchemy import create_engine
import urllib

def get_engine():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=uk_ecommerce;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    encoded = urllib.parse.quote_plus(connection_string)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={encoded}")

def load_data():
    engine = get_engine()

    df_sales = pd.read_sql("SELECT * FROM dbo.fct_sales", engine)
    df_rfm = pd.read_sql("SELECT * FROM dbo.fct_rfm_segments", engine)
    df_cohort = pd.read_sql("SELECT * FROM dbo.fct_cohort", engine)
    df_country = pd.read_sql("SELECT * FROM dbo.fct_country_sales", engine)
    df_raw = pd.read_sql("""
        SELECT description, total_price, quantity, invoice_no
        FROM dbo.stg_transactions
    """, engine)

    # Fix date columns
    df_sales['sales_date'] = pd.to_datetime(df_sales['sales_date'])
    df_cohort['cohort_month'] = pd.to_datetime(df_cohort['cohort_month'])
    df_cohort['cohort_label'] = df_cohort['cohort_month'].dt.strftime('%b %Y')

    print("All tables loaded successfully")
    return df_sales, df_rfm, df_cohort, df_country, df_raw