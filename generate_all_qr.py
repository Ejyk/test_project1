# generate_all_qr.py
import qrcode
import sqlite3
import os

# Folder to save QR images
QR_FOLDER = "qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

# Connect to DB and get store names + referral codes
conn = sqlite3.connect("jobs.db")
c = conn.cursor()
c.execute("SELECT store_name, referral_code FROM hardware_stores")
stores = c.fetchall()
conn.close()

# Generate a QR for each store
for store_name, ref_code in stores:
    url = f"https://app.einstservices.com/Artisan_Register_QR?ref={ref_code}"
    img = qrcode.make(url)
    filename = os.path.join(QR_FOLDER, f"{store_name}_QR.png")
    img.save(filename)
    print(f"Generated QR for {store_name}: {url}")
