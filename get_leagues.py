import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")
url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
querystring = {"country": "England"}  # Optional: filter by country - Example
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

for item in data['response']:
    league = item['league']
    print(f"{league['id']}: {league['name']} ({item['country']['name']})")
