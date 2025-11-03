import sqlite3
import subprocess
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "mnet.db"
SCRAPER_PATH = Path(__file__).resolve().parent / "scrape_mnet_mosids.py"

def get_mnet_mosids():
    """Executes the scraper script and returns a set of MOSID codes."""
    result = subprocess.run(
        ["poetry", "run", "python", str(SCRAPER_PATH)],
        capture_output=True,
        text=True,
        cwd=DB_PATH.parent,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to scrape MNET website: {result.stderr}")

    return {line.split(":")[0] for line in result.stdout.strip().split("\n")}

def get_db_mosids():
    """Connects to the database and returns a set of MOSID codes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT mosid_code FROM mosids")
    return {row[0] for row in cursor.fetchall()}

def main():
    """Compares the MNET website and database MOSID lists and reports discrepancies."""
    print("Fetching MOSIDs from MNET website...")
    mnet_mosids = get_mnet_mosids()
    print(f"Found {len(mnet_mosids)} MOSIDs on the MNET website.")

    print("Fetching MOSIDs from the database...")
    db_mosids = get_db_mosids()
    print(f"Found {len(db_mosids)} MOSIDs in the database.")

    missing_mosids = mnet_mosids - db_mosids

    if not missing_mosids:
        print("\nSuccess! The database contains all MOSIDs found on the MNET website.")
    else:
        print(f"\nFound {len(missing_mosids)} missing MOSIDs in the database:")
        for mosid in sorted(missing_mosids):
            print(f"  - {mosid}")

if __name__ == "__main__":
    main()
