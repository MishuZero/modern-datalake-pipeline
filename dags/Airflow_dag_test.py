from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


with DAG(
        dag_id='bank_transaction_pipeline',
        start_date=datetime(2025, 10, 14),
        schedule='@daily',  # Changed from schedule_interval
        catchup=False,
        tags=['bank', 'transactions']
) as dag:
    def process_transactions():
        print("Processing bank transactions...")


    task = PythonOperator(
        task_id='process_transactions',
        python_callable=process_transactions
    )