import streamlit as st
import pandas as pd
from database import get_connection
from streamlit_autorefresh import st_autorefresh

st.title("📡 Track Your Job")

st_autorefresh(interval=10000)

job_id = st.text_input("Enter your Job ID")

if job_id:
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM jobs WHERE job_id = ?",
        conn,
        params=(job_id,)
    )
    conn.close()

    if df.empty:
        st.error("Job not found")
    else:
        job = df.iloc[0]

        st.subheader("Job Details")
        st.write(f"**Service:** {job.trade}")
        st.write(f"**Location:** {job.location}")

        st.subheader("Status")

        status_map = {
            "Request Sent": "🟡 Request sent to artisans",
            "Accepted": "🔵 Accepted by artisan",
            "In Progress": "🟢 Job in progress",
            "Completed": "✅ Job completed"
        }

        st.info(status_map.get(job.status, job.status))
        st.write(f"**Assigned Artisan:** {job.assigned_artisan or 'Pending'}")
        st.caption(f"Last updated: {job.last_updated}")
