# add_shops.py
from database import get_connection, generate_referral_code
from datetime import datetime

# List of shops
shops = [
    {"name": "Barbing Shop", "email": "barbing@bradford.co.uk", "location": "Bradford"},
    {"name": "UBU", "email": "store2@ubu.co.uk", "location": "Leeds"},
    {"name": "Dirkhill", "email": "store3@dirkhill.co.uk", "location": "Bradford"},
    {"name": "Glocery Shop", "email": "info@einstservices.com", "location": "Bradford"},
]

conn = get_connection()
c = conn.cursor()

for shop in shops:
    referral_code = generate_referral_code()
    artisan_code = f"STORE-{shop['name'].replace(' ', '').upper()}"  # unique internal code
    try:
        c.execute("""
            INSERT INTO artisans (
                artisan_code, business_name, email, phone, trade, location,
                approved, active, created_at, referral_code, referred_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            artisan_code,
            shop['name'],
            shop['email'],
            "",
            "Hardware Store",
            shop['location'],
            1,  # approved
            1,  # active
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            referral_code,
            None
        ))
        print(f"✅ Added {shop['name']} with referral code: {referral_code}")
    except Exception as e:
        print(f"❌ Could not add {shop['name']}: {e}")

conn.commit()
conn.close()
