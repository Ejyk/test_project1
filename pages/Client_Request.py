import streamlit as st
from datetime import datetime
from database import get_connection, generate_unique_job_id
from email_utils import notify_admin

st.title("🛠️ Request a Service")
#st.write("FULL QUERY PARAMS:", st.query_params)
# Capture source from QR code
params = st.query_params
source = params["source"] if "source" in params else "direct"

#st.write("DEBUG SOURCE:", source)

with st.form("client_request"):
    client_name = st.text_input("Your Name")
    client_email = st.text_input("Your Email")

    trade = st.selectbox(
        "Service Needed",
        ["Plumber", "Electrician", "Handyman", "Hairdresser", "Cleaner"]
    )

    location = st.text_input("Your City / Area")
    description = st.text_area("Brief description of the work")

    st.markdown("By submitting, you agree to our legal policies:")
    st.page_link(
        "pages/Artisan_platform_Legal_Policies.py",
        label="📄 Terms of Use, Privacy Policy & Platform Agreements"
    )

    agree = st.checkbox(
        "I agree to the legal policies",
        key="client_agree_terms"
    )

    submit = st.form_submit_button("Send Request")

if submit:
    if not agree:
        st.error("You must agree to the legal policies to continue.")
        st.stop()

    # 🔒 Basic validation
    if not client_name or not client_email or not location or not description:
        st.error("Please fill in all fields (including description).")
        st.stop()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = None

    try:
        conn = get_connection()

        # ✅ Generate 5-character unique Job ID
        job_id = generate_unique_job_id(conn)

        c = conn.cursor()
        c.execute("""
            INSERT INTO jobs (
                job_id,
                client_name,
                client_email,
                trade,
                location,
                status,
                assigned_artisan,
                last_updated,
                description,
		source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            client_name.strip(),
            client_email.strip().lower(),
            trade,
            location.strip().title(),
            "Request Sent",
            None,
            timestamp,
            description.strip(),
            source
        ))

        conn.commit()

        # 🔔 Notify admin
        notify_admin(
            "New Client Request Submitted",
            f"""
New job request received.

Client: {client_name}
Email: {client_email}
Trade: {trade}
Location: {location}
Description: {description}
Job ID: {job_id}
"""
        )

        st.success("✅ Request sent successfully!")
        st.info(f"🆔 Your Job ID: **{job_id}** (save this)")

    except Exception as e:
        st.error("Something went wrong. Please try again.")
        st.exception(e)

    finally:
        if conn:
            conn.close()
