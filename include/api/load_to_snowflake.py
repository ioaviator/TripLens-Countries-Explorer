import snowflake.connector
from .config import url_endpoint, access_key, secret_key, snow_password, snow_account, snow_user
import boto3
import os

ctx = snowflake.connector.connect(
    user=snow_user,
    password=snow_password,
    account=snow_account,
    warehouse='COMPUTE_WH',
    database='TRIPLENS',
    schema='TRIPLENS.RAW'
)

cs = ctx.cursor()

client = boto3.client(
      's3',
      endpoint_url=url_endpoint, # MinIO endpoint
      aws_access_key_id=access_key, # Minio access key
      aws_secret_access_key=secret_key, # Minio secret key
      config=boto3.session.Config(signature_version='s3v4'),
      verify=False # Set to False if using HTTP
    )


def transfer_minio_json_to_snowflake(bucket: str, file_key: str, target_table: str) -> None:

    # Keep just the filename for the local temp path (avoid nested dirs under /tmp)
    filename = os.path.basename(file_key)
    local_temp_path = f"/tmp/{filename}"

    # Download from MinIO -> local temp storage
    client.download_file(bucket, file_key, local_temp_path)

    try:
        # Create file format + internal stage
        cs.execute("USE SCHEMA TRIPLENS.RAW")
        cs.execute("CREATE OR REPLACE FILE FORMAT TRIPLENS_JSON_FMT TYPE = JSON")
        cs.execute("CREATE OR REPLACE STAGE TRIPLENS_STAGE FILE_FORMAT = TRIPLENS_JSON_FMT")
        cs.execute("""
            CREATE OR REPLACE TABLE TRIPLENS.RAW.COUNTRIES_RAW (
                ingestion_ts TIMESTAMP_NTZ,
                src_file STRING,
                payload VARIANT
            );
        """)
        # PUT the local file into the Snowflake internal stage
        # AUTO_COMPRESS can be TRUE (Snowflake will gzip it automatically)
        cs.execute(f"PUT file://{local_temp_path} @TRIPLENS_STAGE AUTO_COMPRESS=TRUE OVERWRITE=TRUE")

        # COPY JSON from stage into target table
        # Loads JSON into a VARIANT column via $1; also captures filename + ingestion time
        cs.execute(f"TRUNCATE TABLE {target_table};")
        cs.execute(f"""
            COPY INTO {target_table} (ingestion_ts, src_file, payload)
            FROM (
              SELECT
                CURRENT_TIMESTAMP(),
                METADATA$FILENAME,
                $1
              FROM @TRIPLENS_STAGE
            )
            FILE_FORMAT = (TYPE = JSON)
            ON_ERROR = 'ABORT_STATEMENT'
        """)

        print(f"Successfully loaded {file_key} into {target_table}")

    finally:
        # Cleanup local file
        if os.path.exists(local_temp_path):
            os.remove(local_temp_path)
