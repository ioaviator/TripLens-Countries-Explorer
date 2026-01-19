from minio import Minio
from .config import url_endpoint, access_key, secret_key
import json
from io import BytesIO

def load_to_bucket(data):
  
  bucket_name = 'final-bucket'
  folder_path = 'raw'
  object_name = f"{folder_path}/countries_raw.json"


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


  data = json.dumps(data, ensure_ascii=False).encode("utf-8")
  data_stream = BytesIO(data)
  data_length = len(data)


  # Upload the data stream
  client.put_object(
    bucket_name=bucket_name,
    object_name=object_name,
    data=data_stream,
    length=data_length,
    content_type="application/json",
  )

  return None  
