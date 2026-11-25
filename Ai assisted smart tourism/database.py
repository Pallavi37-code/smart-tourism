import sqlite3, json
from datetime import datetime
DB_NAME = "smart_tourism.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            start_date TEXT,
            days INTEGER,
            travelers INTEGER,
            budget INTEGER,
            summary TEXT,
            plan_json TEXT,
            created_at TEXT
        )""")

def save_trip(meta, plan):
    with connect() as con:
        con.execute("""INSERT INTO trips(destination,start_date,days,travelers,budget,summary,plan_json,created_at)
        VALUES(?,?,?,?,?,?,?,?)""", (
            meta["destination"], meta["start"], meta["days"], meta["travelers"],
            meta["budget"], plan["summary"], json.dumps(plan), datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

def get_trips():
    with connect() as con:
        rows = con.execute("SELECT id,destination,start_date,days,travelers,budget,summary,created_at FROM trips ORDER BY id DESC").fetchall()
    keys = ["id","destination","start_date","days","travelers","budget","summary","created_at"]
    return [dict(zip(keys,row)) for row in rows]

def delete_trip(trip_id):
    with connect() as con:
        con.execute("DELETE FROM trips WHERE id=?", (trip_id,))
