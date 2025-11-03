from mcp.server.fastmcp import FastMCP
import sqlite3
import yaml
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).resolve().parent.parent / "mnet.db"
DATA_DIR = Path(__file__).resolve().parent / "data"

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
    import json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure repeatable seeding by clearing existing rows before re-population.
    # The order here respects foreign key dependencies (children first).
    for table in (
        "task_statements",
        "noc_equivalencies",
        "mosids",
        "rank_responsibilities",
        "ranks",
    ):
        cursor.execute(f"DELETE FROM {table}")

    # Populate mosids, noc_equivalencies, and task_statements
    with open(DATA_DIR / "mnet_data.json", "r") as f:
        data = json.load(f)
    for mosid_string, noc_data in data.items():
        mosid_code, mosid_title = mosid_string.split(": ", 1)
        cursor.execute("INSERT OR IGNORE INTO mosids (mosid_code, mosid_title) VALUES (?, ?)", (mosid_code, mosid_title))
        cursor.execute("SELECT id FROM mosids WHERE mosid_code = ? AND mosid_title = ?", (mosid_code, mosid_title))
        mosid_id = cursor.fetchone()[0]
        for item in noc_data:
            cursor.execute("INSERT OR IGNORE INTO noc_equivalencies (noc_code, civilian_title, mosid_id) VALUES (?, ?, ?)", (item["noc_code"], item["civilian_title"], mosid_id))
            cursor.execute("SELECT id FROM noc_equivalencies WHERE noc_code = ? AND civilian_title = ? AND mosid_id = ?", (item["noc_code"], item["civilian_title"], mosid_id))
            noc_equivalency_id = cursor.fetchone()[0]
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

# Setup and populate the database on server start
setup_database()
populate_database()


class ASGIEnabledFastMCP(FastMCP):
    """FastMCP variant that can act directly as an ASGI callable."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache the Starlette app so ``__call__`` can delegate to it.
        self._asgi_app = super().streamable_http_app()

    async def __call__(self, scope, receive, send):
        """Let the FastMCP instance behave like an ASGI app."""
        await self._asgi_app(scope, receive, send)

    def streamable_http_app(self):
        """Return the cached ASGI app instead of creating a new one each time."""
        return self._asgi_app


mcp = ASGIEnabledFastMCP("CAF Resume Helper")

def get_rank_data(rank_name: str) -> dict:
    """Return responsibilities for a given rank."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM ranks WHERE rank_name = ?", (rank_name,))
        rank_id_result = cursor.fetchone()
        if not rank_id_result:
            return {}
        rank_id = rank_id_result[0]

        cursor.execute("SELECT responsibility FROM rank_responsibilities WHERE rank_id = ?", (rank_id,))
        responsibilities = [row[0] for row in cursor.fetchall()]

    return {"rank": rank_name, "responsibilities": responsibilities}

def get_mosid_data(mosid_code: str) -> dict:
    """Return NOC equivalencies and task statements for a given MOSID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id, mosid_title FROM mosids WHERE mosid_code = ?", (mosid_code,))
        mosid_row = cursor.fetchone()
        if not mosid_row:
            return {}
        mosid_id, mosid_title = mosid_row

        cursor.execute("SELECT noc_code, civilian_title FROM noc_equivalencies WHERE mosid_id = ?", (mosid_id,))
        noc_equivalencies = cursor.fetchall()

        results = []
        for noc_code, civilian_title in noc_equivalencies:
            cursor.execute(
                """
                SELECT statement FROM task_statements
                JOIN noc_equivalencies ON task_statements.noc_equivalency_id = noc_equivalencies.id
                WHERE noc_equivalencies.noc_code = ? AND noc_equivalencies.mosid_id = ?
                """,
                (noc_code, mosid_id),
            )
            task_statements = [row[0] for row in cursor.fetchall()]
            results.append(
                {
                    "noc_code": noc_code,
                    "civilian_title": civilian_title,
                    "task_statements": task_statements,
                }
            )

    return {"mosid": mosid_code, "title": mosid_title, "equivalencies": results}

def get_mosid_data_batch(mosid_codes: list[str]) -> dict:
    """Return NOC equivalencies and task statements for a given list of MOSIDs."""
    results = {}
    for mosid_code in mosid_codes:
        results[mosid_code] = get_mosid_data(mosid_code)
    return results

mcp.tool()(get_rank_data)
mcp.tool()(get_mosid_data)
mcp.tool()(get_mosid_data_batch)

class BatchMosidRequest(BaseModel):
    """Request payload for MOSID batch lookups."""

    mosid_codes: list[str] = Field(..., min_length=1, max_length=25)


def _not_found(detail: str) -> HTTPException:
    """Return a standardized 404 error."""

    return HTTPException(status_code=404, detail=detail)


mcp_app = mcp.streamable_http_app()


# ``app`` remains the public ASGI callable expected by deployment scripts.
app = FastAPI(title="CAF Resume Helper API", version="1.0.0")


@app.get("/v1/ranks/{rank_name}")
def read_rank(rank_name: str):
    """HTTP endpoint exposing rank responsibilities."""

    data = get_rank_data(rank_name)
    if not data:
        raise _not_found(
            f"Rank {rank_name} is not present in the CAF Resume Helper dataset."
        )
    return data


@app.get("/v1/mosids/{mosid_code}")
def read_mosid(mosid_code: str):
    """HTTP endpoint exposing MOSID equivalency data."""

    data = get_mosid_data(mosid_code)
    if not data:
        raise _not_found(
            f"MOSID code {mosid_code} is not present in the CAF Resume Helper dataset."
        )
    return data


@app.post("/v1/mosids:batchLookup")
def batch_mosid_lookup(request: BatchMosidRequest):
    """HTTP endpoint for batch MOSID lookups."""

    results = {
        mosid_code: data
        for mosid_code in request.mosid_codes
        if (data := get_mosid_data(mosid_code))
    }
    return {"results": results}


app.mount("/mcp", mcp_app)


if __name__ == "__main__":
    mcp.run()
