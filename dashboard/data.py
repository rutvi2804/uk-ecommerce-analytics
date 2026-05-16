import pandas as pd
import os

def load_data():

    # Check if CSV exports exist
    export_path = 'data/exports'

    if os.path.exists(f'{export_path}/fct_sales.csv'):
        print("Loading from CSV exports...")
        df_sales   = pd.read_csv(f'{export_path}/fct_sales.csv')
        df_rfm     = pd.read_csv(f'{export_path}/fct_rfm_segments.csv')
        df_cohort  = pd.read_csv(f'{export_path}/fct_cohort.csv')
        df_country = pd.read_csv(f'{export_path}/fct_country_sales.csv')
        df_raw     = pd.read_csv(f'{export_path}/stg_transactions.csv')

    else:
        print("CSV not found - loading from SQL Server...")
        from sqlalchemy import create_engine
        import urllib

        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=uk_ecommerce;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        encoded = urllib.parse.quote_plus(connection_string)
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={encoded}"
        )

        df_sales   = pd.read_sql(
            "SELECT * FROM dbo.fct_sales", engine)
        df_rfm     = pd.read_sql(
            "SELECT * FROM dbo.fct_rfm_segments", engine)
        df_cohort  = pd.read_sql(
            "SELECT * FROM dbo.fct_cohort", engine)
        df_country = pd.read_sql(
            "SELECT * FROM dbo.fct_country_sales", engine)
        df_raw     = pd.read_sql("""
            SELECT description, total_price, quantity, invoice_no
            FROM dbo.stg_transactions
        """, engine)

    # Fix date columns
    df_sales['sales_date'] = pd.to_datetime(df_sales['sales_date'])
    df_cohort['cohort_month'] = pd.to_datetime(df_cohort['cohort_month'])
    df_cohort['cohort_label'] = (
        df_cohort['cohort_month'].dt.strftime('%b %Y')
    )

    print(f"Sales rows:    {len(df_sales):,}")
    print(f"RFM rows:      {len(df_rfm):,}")
    print(f"Cohort rows:   {len(df_cohort):,}")
    print(f"Country rows:  {len(df_country):,}")
    print(f"Raw rows:      {len(df_raw):,}")
    print("Data loaded successfully")

    return df_sales, df_rfm, df_cohort, df_country, df_raw