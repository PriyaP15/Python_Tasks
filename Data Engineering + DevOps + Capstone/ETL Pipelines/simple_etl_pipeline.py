import pandas as pd
from sqlalchemy import create_engine
import time

MYSQL_URL = "mysql+pymysql://root:root@localhost/etl_db"
POSTGRES_URL = "postgresql+psycopg2://postgres:root@localhost/etl_db"
CSV_FILE = "master_inventory.csv"

def get_data_with_retry(engine, query, retries=3, delay=5):
    count = 0
    while count < retries:
        try:
            return pd.read_sql(query, engine)
        except Exception as e:
            count = count + 1
            print(f"Attempt {count} failed")
            time.sleep(delay)
    raise Exception("Database connection failed")

def databases_to_csv():
    try:
        mysql_engine = create_engine(MYSQL_URL)
        pg_engine = create_engine(POSTGRES_URL)

        mysql_df = get_data_with_retry(mysql_engine, "SELECT * FROM products")
        pg_df = get_data_with_retry(pg_engine, "SELECT * FROM products")

        mysql_df.columns = mysql_df.columns.str.lower()
        pg_df.columns = pg_df.columns.str.lower()

        combined_df = pd.concat([mysql_df, pg_df], ignore_index=True)

        if 'product_id' in combined_df.columns:
            combined_df = combined_df.drop_duplicates(subset=['product_id'], keep='last')
        else:
            print("product_id missing")
            return

        combined_df.to_csv(CSV_FILE, index=False)
        
        print("Completed Successfully")
        print(f"Total rows processed: {len(combined_df)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    databases_to_csv()