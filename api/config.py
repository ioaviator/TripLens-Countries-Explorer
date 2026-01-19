from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# API endpoint only allows for 10 fields for a single api request
# 10+ fields are needed, hence the two url endpoints used
urls = {'url_1': "https://restcountries.com/v3.1/all?fields=name,independent,unMember,startOfWeek,currencies,idd,capital,region,subregion,languages",
        'url_2': "https://restcountries.com/v3.1/all?fields=area,population,continents"}


# create the data_bank folder where json response data is stored locally
parent_dir = Path(__file__).resolve().parent
data_dir = parent_dir / "data_bank"

data_dir.mkdir(parents=True, exist_ok=True)

# MinIO endpoints
url_endpoint = os.getenv('MINIO_ENDPOINT')
access_key = os.getenv('MINIO_ROOT_USER')
secret_key = os.getenv('MINIO_ROOT_PASSWORD')