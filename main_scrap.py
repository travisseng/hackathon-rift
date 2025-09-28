import requests
import json
import sqlite3
import time
import tqdm
from opgg_counter_scraper import fetch_counters
from requests.adapters import HTTPAdapter, Retry

# --- Setup requests session with retries ---
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

roles = ["top", "jungle", "mid", "adc", "support"]

# Fetch all champion names from Data Dragon
url = "https://ddragon.leagueoflegends.com/cdn/15.19.1/data/en_US/champion.json"
data = session.get(url, timeout=10).json()["data"]
champions = data.keys()

# --- Database setup ---
conn = sqlite3.connect("counters.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS champions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS counters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    champion_id INTEGER NOT NULL,
    counter_name TEXT NOT NULL,
    win_rate REAL,
    games INTEGER,
    FOREIGN KEY (champion_id) REFERENCES champions(id)
)
""")
conn.commit()

# --- Main loop ---
db_json = {}
for role in roles:
    db_json[role] = {}
    for champ in tqdm.tqdm(list(champions)):
        tqdm.tqdm.write(f"Scraping {champ} ({role})...")

        # Retry fetch_counters in case of network issues
        for attempt in range(5):
            try:
                counters = fetch_counters(champ, role, session=session)  # pass session
                break
            except requests.exceptions.RequestException as e:
                tqdm.tqdm.write(f"Error fetching {champ} ({role}): {e}. Retrying {attempt+1}/5...")
                time.sleep(2 ** attempt)  # exponential backoff
        else:
            tqdm.tqdm.write(f"Failed to fetch {champ} ({role}) after 5 attempts. Skipping.")
            counters = []

        db_json[role][champ] = counters

        # Insert champion
        cur.execute("INSERT INTO champions (name, role) VALUES (?, ?)", (champ, role))
        champion_id = cur.lastrowid

        # Insert counters
        for counter in counters:
            cur.execute(
                "INSERT INTO counters (champion_id, counter_name, win_rate, games) VALUES (?, ?, ?, ?)",
                (champion_id, counter["name"], counter["win_rate"], counter["games"])
            )
        conn.commit()
        time.sleep(0.5)  # safe delay

# --- Save JSON backup ---
with open("counters.json", "w") as f:
    json.dump(db_json, f, indent=2)

conn.close()
print("Done! Database saved in counters.db and counters.json.")
