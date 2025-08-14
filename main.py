from db import init_db
from fetch_matches import fetch_matches
import sqlite3
init_db()
conn = sqlite3.connect("football_data.db")
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM leagues")
leagues = cursor.fetchall()
conn.close()

seasons = [2022, 2023, 2024, 2025]

for league_id, league_name in leagues:
    for season in seasons:
        print(f"Processing {league_name} ({league_id}) for {season}...")
        fetch_matches(league_id, season)
