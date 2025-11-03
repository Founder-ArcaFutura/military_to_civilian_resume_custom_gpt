import sqlite3
import yaml
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "mnet.db"
DATA_DIR = Path(__file__).resolve().parent.parent / "app" / "data"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mosids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mosid_code TEXT NOT NULL,
            mosid_title TEXT NOT NULL,
            UNIQUE(mosid_code, mosid_title)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noc_equivalencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            noc_code TEXT NOT NULL,
            civilian_title TEXT NOT NULL,
            mosid_id INTEGER NOT NULL,
            FOREIGN KEY (mosid_id) REFERENCES mosids (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_statements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            statement TEXT NOT NULL,
            noc_equivalency_id INTEGER NOT NULL,
            FOREIGN KEY (noc_equivalency_id) REFERENCES noc_equivalencies (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ranks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank_name TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rank_responsibilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            responsibility TEXT NOT NULL,
            rank_id INTEGER NOT NULL,
            FOREIGN KEY (rank_id) REFERENCES ranks (id)
        )
    """)
    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure repeatable seeding by clearing existing rows before re-population.
    for table in (
        "task_statements",
        "noc_equivalencies",
        "mosids",
        "rank_responsibilities",
        "ranks",
    ):
        cursor.execute(f"DELETE FROM {table}")

    # Populate mosids, noc_equivalencies, and task_statements
    with open(DATA_DIR.parent.parent.parent / "data" / "processed" / "mnet_data.json", "r") as f:
        data = json.load(f)
    for mosid_string, noc_data in data.items():
        mosid_code, mosid_title = mosid_string.split(": ", 1)
        cursor.execute("INSERT OR IGNORE INTO mosids (mosid_code, mosid_title) VALUES (?, ?)", (mosid_code, mosid_title))
        cursor.execute("SELECT id FROM mosids WHERE mosid_code = ? AND mosid_title = ?", (mosid_code, mosid_title))
        mosid_id = cursor.fetchone()[0]
        for item in noc_data:
            cursor.execute("INSERT OR IGNORE INTO noc_equivalencies (noc_code, civilian_title, mosid_id) VALUES (?, ?, ?)", (item["noc_code"], item["civilian_title"], mosid_id))
            cursor.execute("SELECT id FROM noc_equivalencies WHERE noc_code = ? AND civilian_title = ? AND mosid_id = ?", (item["noc_code"], item["civilian_title"], mosid_id))
            noc_equivalency_id_result = cursor.fetchone()
            if noc_equivalency_id_result:
                noc_equivalency_id = noc_equivalency_id_result[0]
                for statement in item["task_statements"]:
                    cursor.execute("INSERT OR IGNORE INTO task_statements (statement, noc_equivalency_id) VALUES (?, ?)", (statement, noc_equivalency_id))

    # Populate ranks and rank_responsibilities
    with open(DATA_DIR / "rank_responsibilities.yaml", "r") as f:
        data = yaml.safe_load(f)
    for item in data:
        rank_name = item["rank"]
        cursor.execute("INSERT OR IGNORE INTO ranks (rank_name) VALUES (?)", (rank_name,))
        cursor.execute("SELECT id FROM ranks WHERE rank_name = ?", (rank_name,))
        rank_id = cursor.fetchone()[0]
        for responsibility in item["responsibilities"]:
            cursor.execute("INSERT OR IGNORE INTO rank_responsibilities (responsibility, rank_id) VALUES (?, ?)", (responsibility, rank_id))

    conn.commit()
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    setup_database()
    populate_database()
