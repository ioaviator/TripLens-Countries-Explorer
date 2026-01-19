from minio import Minio
from config import url_endpoint, access_key, secret_key


def load_to_s3():
  
  bucket_name = 'working-bucket'
  folder_path = 'raw'
  object_name = f"{folder_path}/countries_raw.json"

  data_df = 'api/data_bank/countries_data_raw.json'


  client = Minio(
    url_endpoint, # MinIO endpoint
    access_key=access_key, # Minio access key
    secret_key=secret_key, # Minio secret key
    secure=False # Set to False if using HTTP
  )
  
  
  if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
    print(f"Created bucket {bucket_name}")
  else:
    print(f"Bucket {bucket_name} already exists")


  client.fput_object(
    bucket_name,
    object_name,
    data_df,
    content_type="application/json"
  )


load_to_s3()
