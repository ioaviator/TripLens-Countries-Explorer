# from api.extract import api_connect
# from api.load_to_bucket import load_to_bucket
# from api.load_to_snowflake import transfer_minio_json_to_snowflake

# def main():
#   api_response = api_connect()
#   load_to_bucket(api_response)

#   # fp = download_from_bucket()
#   transfer_minio_json_to_snowflake(
#     bucket="final-bucket",
#     file_key="raw/countries_raw.json",
#     target_table="COUNTRIES_RAW",
#   )
#   return None

# main()