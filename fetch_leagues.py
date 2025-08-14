import requests
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()


API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "api-football-v1.p.rapidapi.com"
DB_FILE = "football_data.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

url = f"https://{API_HOST}/v3/leagues"
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

print("Fetching leagues from API...")
response = requests.get(url, headers=headers)
data = response.json()

# === Insert into DB ===
inserted = 0
for item in data.get("response", []):
    league = item.get("league", {})
    country = item.get("country", {})

    league_id = league.get("id")
    name = league.get("name")
    type_ = league.get("type")
    country_name = country.get("name")
    country_code = country.get("code")
    season_start = league.get("season", {}).get("start", "")
    season_end = league.get("season", {}).get("end", "")

    if league_id and name:
        cursor.execute("""
        INSERT OR REPLACE INTO leagues (id, name, type, country, country_code, season_start, season_end)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (league_id, name, type_, country_name, country_code, season_start, season_end))
        inserted += 1

conn.commit()
conn.close()

print(f"Inserted {inserted} leagues into the database.")
