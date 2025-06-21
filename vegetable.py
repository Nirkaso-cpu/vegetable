import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('staff.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vegetables (
    vegetable_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    vegetable_name TEXT,
    vegetable_price TEXT,
    nationality TEXT,
    vegetable_harvest DATE           
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS production (
    production_id INTEGER PRIMARY KEY AUTOINCREMENT,
    production_name TEXT,
    production_popularity TEXT,
    production_delivery DATE
);
""")

with open(
     "r", encoding="utf-8"
) as f:
    vegetables = json.load(f)

    for vegetable in vegetables:

        cursor.execute("""
        INSERT INTO vegetables (
        vegetable_id, vegetable_name, vegetable_price, nationality
        )
        VALUES (?, ?, ?, ?)
""", (
        vegetable["vegetable_id"],
        vegetable["vegetable_name"],
        vegetable["vegetable_price"],
        vegetable["nationality"]
    ))
        
vegetable_id = cursor.lastrowid

cursor.execute("""
            INSERT INTO production (production_id, production_name, production_popularity, production_delivery)
            VALUE (?, ?, ?, ?)              
"""(
    vegetable_id,
    parse_date_safe(vegetable.get("vegetable_harvest")),
    parse_date_safe(vegetable.get("production_delivery"))
))

conn.commit()
conn.close()
