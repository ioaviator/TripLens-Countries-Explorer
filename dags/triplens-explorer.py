from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from include.main  import main as load_data_to_bucket

default_args = {
  'owner': 'Triplens',
  'start_date': datetime(2026, 1, 27),
  'retries': 1,
  'retry_delay': timedelta(minutes=1),
  'schedule': '@hourly'
}

with DAG(
  dag_id='triplens-explorer',
  description='TripLens Countries Explorer', 
  default_args=default_args,
  catchup=False,
  tags=["triplens-explorer", "tourism", "minio", "snowflake", "dbt"],) as dag:

  api_connect = PythonOperator(
    task_id = 'extract_load_to_bucket',
    python_callable = load_data_to_bucket
  )

load_data_to_bucket

