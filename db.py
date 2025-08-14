import sqlite3

def init_db():
    conn = sqlite3.connect('football_data.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            fixture_id INTEGER,
            date TEXT,
            home_team TEXT,
            away_team TEXT,
            home_goals INTEGER,
            away_goals INTEGER,
            league TEXT,
            season INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS leagues (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            country TEXT,
            country_code TEXT,
            season_start TEXT,
            season_end TEXT
        )
    ''')

    conn.commit()
    conn.close()
