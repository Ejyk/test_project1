# 3_Artisan_Accept.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_connection
from email_utils import send_email, notify_admin

st.set_page_config(page_title="Artisan Job Board", layout="centered")



st.title("🛠 Artisan Job Board")

# ----------------------------
# Anti-abuse: simple rate limit
# ----------------------------
if "accept_attempts" not in st.session_state:
    st.session_state.accept_attempts = 0
if "accept_block_until" not in st.session_state:
    st.session_state.accept_block_until = None

if st.session_state.accept_block_until:
    if datetime.now() < st.session_state.accept_block_until:
        st.error("Too many attempts. Please try again later.")
        st.stop()
    else:
        st.session_state.accept_block_until = None
        st.session_state.accept_attempts = 0


# ----------------------------
# Identify artisan (for "My Quote Pending Jobs")
# ----------------------------
st.subheader("🔐 Identify Yourself (Approved Artisans)")
artisan_code_lookup = st.text_input("Enter your Artisan ID", key="artisan_code_lookup")

artisan_name_lookup = None

if artisan_code_lookup.strip():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT business_name
        FROM artisans
        WHERE artisan_code = ?
          AND approved = 1
          AND active = 1
    """, (artisan_code_lookup.strip().upper(),))
    row = c.fetchone()
    conn.close()

    if not row:
        st.error("Artisan ID not found or not approved.")
    else:
        artisan_name_lookup = row[0]
        st.success(f"Welcome, **{artisan_name_lookup}** ✅")

# ----------------------------
# Section A: Open jobs (public)
# ----------------------------
st.divider()
st.subheader("📌 Open Jobs (Request Sent)")

conn = get_connection()
jobs_open = pd.read_sql(
    "SELECT job_id, trade, location, description FROM jobs WHERE status = 'Request Sent'",
    conn
)
conn.close()

if jobs_open.empty:
    st.info("No open jobs available right now.")
else:
    st.caption("Jobs are allocated on a first-come-first-serve basis.")
    for _, job in jobs_open.iterrows():
        st.write(f"**Job ID:** {job.job_id} — {job.trade} | {job.location}")
        st.caption(f"📝 {job.description or 'No description provided'}")

# ----------------------------
# Section B: My accepted jobs (quote pending)
# ----------------------------
st.divider()
st.subheader("🟣 My Accepted Jobs (Quote Pending)")

if artisan_name_lookup is None:
    st.info("Enter your Artisan ID above to see your quote-pending jobs.")
else:
    conn = get_connection()
    my_pending = pd.read_sql(
        """
        SELECT job_id, trade, location, description, last_updated
        FROM jobs
        WHERE status = 'Accepted - Quote Pending'
          AND assigned_artisan = ?
        ORDER BY last_updated DESC
        """,
        conn,
        params=(artisan_name_lookup,)
    )
    conn.close()

    if my_pending.empty:
        st.info("You have no quote-pending jobs.")
    else:
        for _, job in my_pending.iterrows():
            st.write(f"**Job ID:** {job.job_id} — {job.trade} | {job.location}")
            st.caption(f"📝 {job.description or 'No description provided'}")
            st.caption(f"Last updated: {job.last_updated}")

            if st.button(
                f"📤 Mark Quote Sent (Job {job.job_id})",
                key=f"quote_sent_{job.job_id}"
            ):
                conn = get_connection()
                c = conn.cursor()

                c.execute("""
                    UPDATE jobs
                    SET status = ?, last_updated = ?
                                       
                    WHERE job_id = ? AND status = 'Accepted - Quote Pending' AND assigned_artisan = ?
                   
                """, (
                    "Quote Sent to Admin",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    job.job_id,
                    artisan_name_lookup
                ))
                conn.commit()

                if c.rowcount == 1:
                    notify_admin(
                        "📨 Quote Sent by Artisan",
                        f"""
An artisan marked a quote as sent.

Job ID: {job.job_id}
Trade: {job.trade}
Location: {job.location}
Description: {job.description}

Artisan: {artisan_name_lookup}

ACTION: Contact artisan for quote details and update the client.
"""
                    )
                    st.success("✅ Quote marked as sent. Admin has been notified.")
                else:
                    st.error("Unable to update job status.")

                conn.close()
                st.rerun()

# ----------------------------
# Accept a job (requires verified identity + Job ID)
# ----------------------------
st.divider()
st.subheader("✅ Accept a Job")

# Must identify first
if artisan_name_lookup is None:
    st.warning("Please identify yourself above before accepting a job.")
    st.stop()

job_id_to_accept = st.text_input("Enter Job ID", key="accept_job_id")

if st.button("Confirm Accept", key="confirm_accept"):
    st.session_state.accept_attempts += 1

    if st.session_state.accept_attempts > 5:
        st.session_state.accept_block_until = datetime.now() + timedelta(minutes=10)
        st.error("Too many attempts. Locked for 10 minutes.")
        st.stop()

    if not job_id_to_accept.strip():
        st.error("Enter the Job ID.")
        st.stop()

    job_id_to_accept = job_id_to_accept.strip()
    artisan_name = artisan_name_lookup
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    c = conn.cursor()

    # ✅ Atomic accept (first-come-first-serve)
    c.execute("""
        UPDATE jobs
        SET status = ?, assigned_artisan = ?, last_updated = ?
        WHERE job_id = ? AND status = 'Request Sent'
    """, ("Accepted - Quote Pending", artisan_name, now, job_id_to_accept))
    conn.commit()

    if c.rowcount != 1:
        conn.close()
        st.error("Job already taken or Job ID invalid.")
        st.stop()

    # Fetch client/job info for email + admin
    c.execute("""
        SELECT client_name, client_email, trade, location, description
        FROM jobs
        WHERE job_id = ?
    """, (job_id_to_accept,))
    row = c.fetchone()
    conn.close()

    if not row:
        st.error("Could not load job details. Please try again.")
        st.stop()

    client_name, client_email, trade, location, description = row

    subject = "Update: An artisan has accepted your request (Quote Pending)"
    message = f"""
Hello {client_name},

Good news — an artisan has accepted your request.

Next step: We are confirming a quote and will contact you shortly.

Service: {trade}
Location: {location}
Assigned artisan: {artisan_name}
Job ID: {job_id_to_accept}

Thank you.
"""

    try:
        send_email(client_email, subject, message)

        notify_admin(
            "✅ Job Accepted by Artisan (Quote Pending)",
            f"""
A job has been accepted (Quote Pending).

Job ID: {job_id_to_accept}
Trade: {trade}
Location: {location}
Description: {description}

Client: {client_name} ({client_email})
Accepted by: {artisan_name}
Time: {now}

ACTION: Contact the artisan to collect a quote, then update the client.
"""
        )

        st.success("✅ Job accepted. Client notified and admin alerted by email.")
    except Exception as e:
        st.warning("Job accepted, but email notification failed.")
        st.exception(e)

    st.session_state.accept_attempts = 0
    st.session_state.accept_block_until = None
    st.rerun()

