import requests
import sqlite3
import time
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "api-football-v1.p.rapidapi.com"
DB_FILE = "football_data.db"

def fetch_matches(league_id, season):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print(f"Fetching matches for League ID {league_id}, Season {season}...")

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    url = f"https://{API_HOST}/v3/fixtures"
    params = {"league": league_id, "season": season}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
    except Exception as e:
        print(f"Error fetching matches for league {league_id}: {e}")
        return

    response_data = data.get("response", [])
    if response_data:
        league_info = response_data[0].get("league", {})
        league_name = league_info.get("name", f"League {league_id}")
    else:
        league_name = f"League {league_id}"

    inserted = 0
    for match in response_data:
        fixture = match.get("fixture", {})
        teams = match.get("teams", {})
        goals = match.get("goals", {})

        fixture_id = fixture.get("id")
        date = fixture.get("date")
        home_team = teams.get("home", {}).get("name")
        away_team = teams.get("away", {}).get("name")
        home_goals = goals.get("home")
        away_goals = goals.get("away")

        if home_team and away_team:
            cursor.execute("""
            INSERT OR REPLACE INTO matches (
                fixture_id, date, home_team, away_team, home_goals, away_goals, league, season
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fixture_id, date, home_team, away_team, home_goals, away_goals, league_name, season
            ))
            inserted += 1

    conn.commit()
    conn.close()

    print(f"Inserted or updated {inserted} matches for {league_name} ({season})")
    

    time.sleep(1)  # Respect rate limits
