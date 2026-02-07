import os
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from include.api.extract import api_connect
from include.api.load_to_bucket import load_to_bucket
from include.api.load_to_snowflake import transfer_minio_json_to_snowflake
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from airflow.decorators import task 



DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
execution_config = ExecutionConfig(
    dbt_executable_path = DBT_EXECUTABLE_PATH
)

DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt/dbt_triplens"
project_config = ProjectConfig(
   dbt_project_path= DBT_PROJECT_PATH,
   manifest_path=f"{DBT_PROJECT_PATH}/target/manifest.json",
)

profile_config = ProfileConfig(
  profile_name='default',
  target_name='dev',
  profile_mapping=SnowflakeUserPasswordProfileMapping(
    conn_id="snowflake_conn",
    profile_args={'database': 'triplens', 'schema': 'raw'},
  ),
)

default_args = {
  'owner': 'Triplens',
  'start_date': datetime(2026, 1, 27),
  'retries': 1,
  'retry_delay': timedelta(minutes=1),
  'schedule': '@hourly'
}


@task()
def extract_data_from_api():
  api_response = api_connect()
  return api_response

@task()
def load_data_to_s3(api_response):
  load_to_bucket(api_response)

@task()
def transfer_to_snowflake():
  transfer_minio_json_to_snowflake(
    bucket="final-bucket",
    file_key="raw/countries_raw.json",
    target_table="COUNTRIES_RAW",
  )


with DAG(
  dag_id='triplens-explorer',
  description='TripLens Countries Explorer', 
  default_args=default_args,
  catchup=False,
  tags=["triplens-explorer", "tourism", "minio", "snowflake", "dbt"],
  ) as dag:
    
    api_response = extract_data_from_api()
    
    dbt_snowflake_dag = DbtTaskGroup(
      group_id='transform_data',
      project_config=project_config,
      profile_config=profile_config,
      execution_config=execution_config,
      default_args=default_args
    )

    # task dependencies
    (
      api_response 
      >> load_data_to_s3(api_response) 
      >> transfer_to_snowflake()
      >> dbt_snowflake_dag
    )
