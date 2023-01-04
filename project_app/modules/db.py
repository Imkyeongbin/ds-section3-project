import os
# import psycopg2
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

host = os.environ.get("DATABASE_HOST")
port = os.environ.get("DATABASE_PORT")
dbname = os.environ.get("DATABASE_DBNAME")
username = os.environ.get("DATABASE_USERNAME")
password = os.environ.get("DATABASE_PASSWORD")

url = URL.create(
    drivername="postgresql",
    username=username,
    host=host,
    database=dbname,
    password=password
)
# conn_string = f"host='{host}' dbname='{dbname}' user='{username}' password='{password}'"

def get_engine():
    return create_engine(url)

def recreate_table():
    engine = get_engine()
    engine.execute("DROP TABLE IF EXISTS dataset")
    engine.execute("""
        CREATE TABLE IF NOT EXISTS dataset (
            id int NULL,
            gender varchar NULL,
            age int NULL,
            hypertension int NULL,
            heart_disease int NULL,
            ever_married varchar NULL,
            work_type varchar NULL,
            Residence_type varchar NULL,
            avg_glucose_level float8 NULL,
            bmi float8 NULL,
            smoking_status varchar NULL,
            stroke int NULL,
            CONSTRAINT dataset_pk PRIMARY KEY (id)
        );
    """)
    print("Table is recreated")
