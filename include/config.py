import os
from dotenv import load_dotenv

load_dotenv()

# API endpoint only allows for 10 fields for a single api request
# 10+ fields are needed, hence the two url endpoints used
urls = {'url_1': "https://restcountries.com/v3.1/all?fields=name,independent,unMember,startOfWeek,currencies,idd,capital,region,subregion,languages",
        'url_2': "https://restcountries.com/v3.1/all?fields=area,population,continents"}



# MinIO endpoints
url_endpoint = os.getenv('MINIO_ENDPOINT', 'http://localhost:9000')
access_key = os.getenv('MINIO_ROOT_USER')
secret_key = os.getenv('MINIO_ROOT_PASSWORD')
snow_user = os.getenv('SNOW_USER')
snow_password = os.getenv('SNOW_PASSWORD')
snow_account = os.getenv('SNOW_ACCOUNT')
