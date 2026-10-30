# pages/Artisan_Register.py
import streamlit as st
import sqlite3
import random
import string

st.set_page_config(page_title="Artisan Registration", page_icon="🛠️")
st.title("Einst Personnel Management Services (EPMS) Ltd\nArtisan Registration")

# --- Utility: Generate unique Artisan Code ---
def generate_artisan_code():
    prefix = "EPMS"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{suffix}"

# --- Manual Registration Form ---
with st.form("manual_registration_form"):
    business_name = st.text_input("Business Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    trade = st.selectbox(
        "Trade",
        ["Plumber", "Electrician", "Cleaner", "Gas Engineer", "Handyman", "Other"]
    )
    business_address = st.text_input("Business Address")
    location = st.text_input("City / Area")
    postcode = st.text_input("Postcode (optional)")

    gas_safe_number = None
    if trade in ["Plumber", "Gas Engineer"]:
        gas_safe_number = st.text_input("🔥 Gas Safe Registration Number")

    referral_code = st.text_input("Referral Code (optional)")

    submitted = st.form_submit_button("Register")

    if submitted:
        artisan_code = generate_artisan_code()

        # Save to database
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO artisans 
            (business_name, email, phone, trade, business_address, location, postcode, gas_safe_number, artisan_code, referral_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            business_name,
            email,
            phone,
            trade,
            business_address,
            location,
            postcode,
            gas_safe_number,
            artisan_code,
            None
        ))
        conn.commit()
        conn.close()

        st.success(f"✅ Registration successful! Your Artisan Code: {artisan_code}")
