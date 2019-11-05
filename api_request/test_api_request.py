import requests
import pprint
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('api_key')

r = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t=joker")
data = r.json()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)
#print(data['Writer'])


