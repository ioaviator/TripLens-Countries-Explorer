from .config import url_endpoint, access_key, secret_key
import json
import boto3
from botocore.exceptions import ClientError

def load_to_bucket(data):
  
  bucket_name = 'final-bucket'
  folder_path = 'raw'
  object_name = f"{folder_path}/countries_raw.json"


  client = boto3.client(
    's3',
    endpoint_url=url_endpoint, # MinIO endpoint
    aws_access_key_id=access_key, # Minio access key
    aws_secret_access_key=secret_key, # Minio secret key
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False # Set to False if using HTTP
  )
  
    # check if bucket exists and create it if not
  try:
    client.head_bucket(Bucket=bucket_name)
    print(f'Bucket {bucket_name} already exists')
  except ClientError as e:
    if e.response['Error']['Code'] == '404':
      client.create_bucket(Bucket=bucket_name)
      print(f'{bucket_name} created')

  data = json.dumps(data, ensure_ascii=False).encode("utf-8")

  # Upload the data stream
  client.put_object(
    Bucket=bucket_name,
    Key=object_name,
    Body=data,
    ContentType="application/json",
  )

  return None  
