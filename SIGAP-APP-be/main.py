from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import asyncio
from datetime import datetime, timedelta
import pytz

import scrape_detail_and_analyze 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    if table_name not in ALL_TABLES:
        raise HTTPException(status_code=404, detail="Portal tidak ditemukan")

    data = fetch_all_from_table(table_name)
    return {"portal": table_name, "data": data}


# === Jadwal Scraping Otomatis ===

async def schedule_scraping():
    while True:
        now = datetime.now(pytz.timezone('Asia/Jakarta'))
        target = now.replace(hour=3, minute=0, second=0, microsecond=0)

        if now >= target:
            target += timedelta(days=1)

        wait_time = (target - now).total_seconds()
        print(f"[Scheduler] Waiting {wait_time:.2f} seconds until next scraping at {target.hour:02d}:{target.minute:02d} WIB...")

        await asyncio.sleep(wait_time)

        print("[Scheduler] Running daily scraping task...")
        scrape_detail_and_analyze.main()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(schedule_scraping())
