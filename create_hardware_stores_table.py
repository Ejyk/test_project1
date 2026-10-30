# create_hardware_stores_table.py
import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS hardware_stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL,
    referral_code TEXT NOT NULL UNIQUE
)
""")

# Example stores
stores = [
    ("Shop1", "SHOP001"),
    ("Shop2", "SHOP002"),
    ("Shop3", "SHOP003")
]

# Insert stores (ignore if already exists)
for store_name, referral_code in stores:
    c.execute("""
    INSERT OR IGNORE INTO hardware_stores (store_name, referral_code)
    VALUES (?, ?)
    """, (store_name, referral_code))

conn.commit()
conn.close()

print("hardware_stores table created and sample stores inserted.")
