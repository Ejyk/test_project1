import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_connection
from email_utils import send_email
from auth import admin_login_required

st.set_page_config(page_title="Admin Panel", layout="centered")




st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #e3f2fd; }
</style>
""", unsafe_allow_html=True)

admin_login_required()
st.title("🛠 Admin / Operations Panel")

# ----------------------------
# 1) APPROVE ARTISANS
# ----------------------------
st.subheader("✅ Approve Artisans")

conn = get_connection()
pending = pd.read_sql("""
    SELECT artisan_id, artisan_code, business_name, email, trade, location, created_at
    FROM artisans
    WHERE approved = 0 AND active = 1
    ORDER BY created_at DESC
""", conn)
conn.close()

if pending.empty:
    st.info("No pending artisan registrations.")
else:
    for _, a in pending.iterrows():
        st.write(f"**{a.business_name}** | {a.trade} | {a.location} | {a.email}")

        if st.button(f"Approve {a.business_name}", key=f"approve_{a.artisan_id}"):

            # Approve + ensure active
            conn = get_connection()
            c = conn.cursor()
            c.execute("""
                UPDATE artisans
                SET approved = 1, active = 1
                WHERE artisan_id = ?
            """, (a.artisan_id,))
            conn.commit()
            conn.close()

            # Email artisan their public ID
            try:
                send_email(
                    a.email,
                    "✅ EPMS Approved – Your Artisan ID",
                    f"""
Hello {a.business_name},

Your registration has been approved ✅

Your Artisan ID is: {a.artisan_code}

IMPORTANT:
• Save this ID somewhere safe.
• You will use it to identify yourself and accept jobs inside the app.

Thanks,
EPMS Admin
"""
                )
                st.success(f"{a.business_name} approved ✅ (ID sent by email)")
            except Exception as e:
                st.warning("Approved, but failed to email the artisan.")
                st.exception(e)

            st.rerun()

st.divider()

# ----------------------------
# 2) VIEW / SEARCH / DEACTIVATE ARTISANS
# ----------------------------
st.subheader("📋 Registered Artisans")

search = st.text_input("Search by name, email, trade, location, or Artisan ID")

conn = get_connection()
df = pd.read_sql("""
    SELECT artisan_id, artisan_code, business_name, email, phone, trade, location, approved, active, created_at
    FROM artisans
    ORDER BY created_at DESC
""", conn)
conn.close()

if search.strip():
    s = search.strip().lower()
    df = df[
        df["artisan_code"].fillna("").str.lower().str.contains(s) |
        df["business_name"].fillna("").str.lower().str.contains(s) |
        df["email"].fillna("").str.lower().str.contains(s) |
        df["trade"].fillna("").str.lower().str.contains(s) |
        df["location"].fillna("").str.lower().str.contains(s)
    ]

if df.empty:
    st.info("No artisans found.")
else:
    st.dataframe(df.drop(columns=["artisan_id"]), use_container_width=True)

    st.caption("Deactivate an artisan instead of deleting (safer for records).")

    artisan_to_deactivate = st.selectbox(
        "Select artisan to deactivate",
        df["artisan_code"].tolist()
    )

    if st.button("Deactivate Artisan"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            UPDATE artisans
            SET active = 0
            WHERE artisan_code = ?
        """, (artisan_to_deactivate,))
        conn.commit()
        conn.close()
        st.success(f"Artisan {artisan_to_deactivate} deactivated ✅")
        st.rerun()

st.divider()

# ----------------------------
# 3) CREATE JOB REQUEST + NOTIFY ARTISANS
# ----------------------------
st.subheader("📩 Create Job Request")

with st.form("job_form"):
    client_name = st.text_input("Client Name")
    client_email = st.text_input("Client Email (optional)")
    client_address = st.text_input("Client Address")
    trade = st.selectbox("Trade Needed", ["Plumber", "Electrician", "Handyman"])
    location = st.text_input("Location (e.g., Bradford, Leeds)")

    submitted = st.form_submit_button("Find Matching Artisans")

if submitted:
    if not client_name or not client_address or not location:
        st.error("Please fill client name, address, and location.")
        st.stop()

    normalized_location = location.strip().title()

    conn = get_connection()
    artisans = pd.read_sql("""
        SELECT business_name, email
        FROM artisans
        WHERE approved = 1 AND active = 1
          AND trade = ?
          AND location = ?
    """, conn, params=(trade, normalized_location))
    conn.close()

    if artisans.empty:
        st.warning("No approved artisans found for this trade and location.")
        st.stop()

    st.success(f"Found {len(artisans)} matching artisan(s). Select who to notify:")

    with st.form("notify_form"):
        selected = st.multiselect(
            "Select artisans to notify",
            artisans["business_name"].tolist(),
            default=artisans["business_name"].tolist()
        )
        send_now = st.form_submit_button("Send Emails Now")

    if send_now:
        if not selected:
            st.error("Select at least one artisan.")
            st.stop()

        sent = 0
        for name in selected:
            to_email = artisans.loc[artisans["business_name"] == name, "email"].values[0]

            subject = "New Job Request Available"
            message = f"""
Hello {name},

A new job request is available.

Client: {client_name}
Address: {client_address}
Trade: {trade}
Location: {normalized_location}

This job will be assigned on a first-come-first-serve basis.

Please check the Artisan Job Board to accept the job.
"""
            try:
                send_email(to_email, subject, message)
                sent += 1
            except Exception as e:
                st.warning(f"Could not send to {name}: {e}")

        st.success(f"✅ Sent {sent} email(s).")
