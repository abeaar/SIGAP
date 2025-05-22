from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()
DB_PATH = "./database/news.db"

TERKINI_TABLES = ["detik", "kedaulatanrakyat", "times"]
TERPOPULER_TABLES = ["detik_popular", "idntimes_popular", "kedaulatanrakyat_popular", "times_popular"]

ALL_TABLES = TERKINI_TABLES + TERPOPULER_TABLES

def fetch_all_from_table(table_name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except sqlite3.Error:
        return []
    finally:
        conn.close()

@app.get("/terkini")
def get_terkini_news():
    result = []
    for table in TERKINI_TABLES:
        data = fetch_all_from_table(table)
        for d in data:
            d["portal"] = table
        result.extend(data)
    return {"terkini": result}

@app.get("/terpopuler")
def get_terpopuler_news():
    result = []
    for table in TERPOPULER_TABLES:
        data = fetch_all_from_table(table)
        for d in data:
            d["portal"] = table
        result.extend(data)
    return {"terpopuler": result}

@app.get("/news/{portal}")
def get_news_by_portal(portal: str):
    table_name = portal.lower()

    valid_tables = ALL_TABLES
    if table_name not in valid_tables:
        raise HTTPException(status_code=404, detail="Portal tidak ditemukan")

    data = fetch_all_from_table(table_name)
    return {"portal": table_name, "data": data}
