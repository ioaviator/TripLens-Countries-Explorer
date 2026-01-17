from pathlib import Path


# API endpoint only allows for 10 fields for a single api request
# 10 fields are needed, hence the two url endpoints used
urls = {'url_1': "https://restcountries.com/v3.1/all?fields=name,independent,unMember,startOfWeek,currencies,idd,capital,region,subregion,languages",
        'url_2': "https://restcountries.com/v3.1/all?fields=area,population,continents"}


#  resolve directory path
parent_dir = Path(__file__).resolve().parent
data_dir = parent_dir / "data_bank"

data_dir.mkdir(parents=True, exist_ok=True)
