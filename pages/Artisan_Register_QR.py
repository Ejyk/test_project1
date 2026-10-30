# pages/Artisan_Register_QR.py

import streamlit as st
import sqlite3
import random
import string
import re

# ---------------------------
# ✅ Validators
# ---------------------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 15

def is_valid_postcode(postcode):
    if postcode == "":
        return True
    pattern = r"^[A-Za-z0-9 ]{5,8}$"
    return re.match(pattern, postcode)

# ---------------------------
# ✅ Page Setup
# ---------------------------
st.set_page_config(page_title="Artisan Registration via QR", page_icon="🛠️")
st.title("Einst Personnel Management Services (EPMS) Ltd\nArtisan Registration (QR)")

# ---------------------------
# ✅ Generate unique Artisan Code
# ---------------------------
def generate_artisan_code():
    prefix = "EPMS"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{suffix}"

# ---------------------------
# ✅ Capture referral code from QR URL
# ---------------------------


query_params = st.query_params
ref_code_from_qr = query_params.get("ref", "")

# ✅ Validate format: SHOP001, SHOP002, etc.
if re.match(r"^SHOP\d{3}$", ref_code_from_qr):
    st.session_state["ref_code"] = ref_code_from_qr
else:
    st.session_state["ref_code"] = ""

if "ref_code" not in st.session_state:
    st.session_state["ref_code"] = ref_code_from_qr

referred_by = st.session_state.get("ref_code", "")

# ---------------------------
# ✅ Registration Form
# ---------------------------
with st.form("registration_form"):
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

    st.text_input(
        "Referral Code (from Hardware Store)",
        value=referred_by,
        disabled=True
    )

    gas_safe_number = None
    if trade in ["Plumber", "Gas Engineer"]:
        gas_safe_number = st.text_input("🔧 Gas Safe Registration Number")

    submitted = st.form_submit_button("Register")

# ---------------------------
# ✅ Form Submission
# ---------------------------
if submitted:

    # --- Required fields
    if not business_name or not email or not phone or not location:
        st.error("❌ Please fill in all required fields")
        st.stop()

    if not is_valid_email(email):
        st.error("❌ Invalid email address")
        st.stop()

    if not is_valid_phone(phone):
        st.error("❌ Invalid phone number")
        st.stop()

    if not is_valid_postcode(postcode):
        st.error("❌ Invalid postcode")
        st.stop()

    # ---------------------------
    # ✅ Open DB
    # ---------------------------
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    # --- Prevent duplicate email
    c.execute("SELECT * FROM artisans WHERE email = ?", (email,))
    if c.fetchone():
        st.error("❌ This email is already registered")
        conn.close()
        st.stop()

    # --- Generate artisan code
    artisan_code = generate_artisan_code()

    # ---------------------------
    # ✅ Insert into DB
    # ---------------------------
    c.execute("""
        INSERT INTO artisans
        (business_name, email, phone, trade, business_address, location,
         postcode, gas_safe_number, artisan_code, referral_code, referred_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        business_name,
        email,
        phone,
        trade,
        business_address,
        location,
        postcode,
        gas_safe_number,
        artisan_code,      # artisan's unique ID
        artisan_code,                # placeholder for referral_code if artisan gets one
        referred_by        # referral code from QR
    ))

    conn.commit()
    conn.close()

    st.success(f"✅ Registration successful! Your Artisan Code: **{artisan_code}**")
