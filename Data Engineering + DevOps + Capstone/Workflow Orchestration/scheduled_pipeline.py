import os
import shutil
import pandas as pd
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine

INBOUND_DIR = "/opt/airflow/inputs"
ARCHIVE_DIR = "/opt/airflow/archive"
STAGING_FILE = "/opt/airflow/staging_data.csv"
CLEAN_FILE = "/opt/airflow/clean_customers.csv"

def extract_customer_data():
    files = os.listdir(INBOUND_DIR)
    target_file = None
    for f in files:
        if f.lower().endswith(".csv"):
            target_file = f
            break 
    if target_file is None:
        raise FileNotFoundError(f"No CSV found in {INBOUND_DIR}!")
    df = pd.read_csv(os.path.join(INBOUND_DIR, target_file))
    df.to_csv(STAGING_FILE, index=False)
    return target_file

def transform_customer_data(ti):
    df = pd.read_csv(STAGING_FILE)
    new_cols = []
    for col in df.columns:
        new_cols.append(col.strip())
    df.columns = new_cols

    for col in ["Units Sold", "Total Sales"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].mean()).round(2)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_cleaned = df.dropna(subset=["Date", "Total Sales"])
    df_cleaned.to_csv(CLEAN_FILE, index=False)
    return CLEAN_FILE

def load_to_postgres(ti):
    conn_str = "postgresql://airflow:airflow@postgres:5432/airflow"
    engine = create_engine(conn_str)
    file_to_load = ti.xcom_pull(task_ids='transform_step')
    df = pd.read_csv(file_to_load)
    df.to_sql('sales_records', engine, if_exists='append', index=False)

def archive_file(ti):
    filename = ti.xcom_pull(task_ids='extract_step')
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    shutil.move(os.path.join(INBOUND_DIR, filename), os.path.join(ARCHIVE_DIR, filename))

with DAG(
    dag_id='postgres_etl_v2',
    schedule='@daily',
    start_date=datetime(2026, 3, 1),
    catchup=False,
) as dag:

    extract = PythonOperator(task_id='extract_step', python_callable=extract_customer_data)
    transform = PythonOperator(task_id='transform_step', python_callable=transform_customer_data)
    load = PythonOperator(task_id='load_step', python_callable=load_to_postgres)
    archive = PythonOperator(task_id='archive_step', python_callable=archive_file)

    extract >> transform >> load >> archive