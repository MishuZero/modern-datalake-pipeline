import pandas as pd
from faker import Faker
import random
from datetime import datetime
import os
import boto3

from airflow.decorators import dag, task

# --- DAG Configuration ---
MINIO_ENDPOINT = "http://minio:9000"   # service name from docker-compose
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET_NAME = "banking-data"  # make sure this bucket exists
NUMBER_OF_CUSTOMERS = 1000

# Local file paths for intermediate storage on the Airflow worker
LOCAL_CUSTOMERS_FILE = "/tmp/customers.csv"
LOCAL_TRANSACTIONS_FILE = "/tmp/transactions.csv"


@dag(
    dag_id="generate_banking_data_to_minio",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["minio", "data-generation"],
    doc_md="""
    ### Banking Data Generation DAG
    This DAG generates fake customer and transaction data and uploads it to a MinIO bucket.
    """
)
def generate_banking_data_dag():
    """ETL DAG to Generate and Upload Fake Banking Data"""

    @task
    def generate_customers_data() -> str:
        """Generate fake customer data and save it to a local CSV."""
        print(f"Generating {NUMBER_OF_CUSTOMERS} fake customer records.")
        fake = Faker()
        customers = [
            {
                "customer_id": i + 1,
                "name": fake.name(),
                "address": fake.address().replace("\n", ", "),
                "email": fake.email(),
                "join_date": fake.date_this_decade()
            }
            for i in range(NUMBER_OF_CUSTOMERS)
        ]

        df = pd.DataFrame(customers)
        df.to_csv(LOCAL_CUSTOMERS_FILE, index=False)
        print(f"✅ Customer data saved locally to {LOCAL_CUSTOMERS_FILE}")
        return LOCAL_CUSTOMERS_FILE

    @task
    def generate_transactions_data(customer_file_path: str) -> str:
        """Generate fake transaction data for each customer."""
        print(f"Reading customer data from {customer_file_path}")
        customers_df = pd.read_csv(customer_file_path)
        customer_ids = customers_df["customer_id"].tolist()

        fake = Faker()
        transactions = []
        transaction_id_counter = 1

        print("Generating transaction data...")
        for cid in customer_ids:
            for _ in range(random.randint(5, 50)):
                transactions.append({
                    "transaction_id": transaction_id_counter,
                    "customer_id": cid,
                    "amount": round(random.uniform(5.5, 1000.0), 2),
                    "transaction_date": fake.date_time_this_year(),
                    "type": random.choice(["DEBIT", "CREDIT"])
                })
                transaction_id_counter += 1

        df = pd.DataFrame(transactions)
        df.to_csv(LOCAL_TRANSACTIONS_FILE, index=False)
        print(f"✅ Transaction data saved locally to {LOCAL_TRANSACTIONS_FILE}")
        return LOCAL_TRANSACTIONS_FILE

    @task
    def upload_to_minio(file_path: str, object_name: str):
        """Upload a file to MinIO using boto3."""
        print(f"📤 Uploading {file_path} to MinIO bucket '{MINIO_BUCKET_NAME}' as '{object_name}'")

        s3_client = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name="us-east-1",
        )

        try:
            s3_client.upload_file(file_path, MINIO_BUCKET_NAME, object_name)
            print("✅ Upload successful!")
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise

    @task
    def cleanup_local_files(files_to_delete: list):
        """Remove temporary files from the local filesystem."""
        print(f"🧹 Cleaning up local files: {files_to_delete}")
        for f in files_to_delete:
            if os.path.exists(f):
                os.remove(f)
                print(f"Removed {f}")

    # --- Define Task Dependencies ---
    customers_file = generate_customers_data()
    transactions_file = generate_transactions_data(customers_file)

    upload_customers = upload_to_minio(customers_file, "customers/customer_data.csv")
    upload_transactions = upload_to_minio(transactions_file, "transactions/transaction_data.csv")

    cleanup_local_files([customers_file, transactions_file]).set_upstream([
        upload_customers,
        upload_transactions
    ])


# Instantiate the DAG
generate_banking_data_dag()
