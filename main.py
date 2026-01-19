from api.extract import api_connect
from api.load_to_bucket import load_to_bucket


def main():
  api_response = api_connect()
  load_to_bucket(api_response)

  return None



if __name__ == '__main__':
  main()