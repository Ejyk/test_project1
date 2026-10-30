import streamlit as st
import pandas as pd
from database import get_connection
from auth import admin_login_required  # remove if you don’t use auth


st.set_page_config(page_title="Admin – Manage Artisans", layout="wide")
admin_login_required()



st.title("🛡 Admin – Manage Artisans")

# ----------------------------
# Ensure artisans.active column exists (soft delete support)
# ----------------------------
def ensure_active_column():
    conn = get_connection()
    c = conn.cursor()
    c.execute("PRAGMA table_info(artisans)")
    cols = [row[1] for row in c.fetchall()]
    if "active" not in cols:
        c.execute("ALTER TABLE artisans ADD COLUMN active INTEGER DEFAULT 1")
        conn.commit()
    conn.close()

ensure_active_column()

# ----------------------------
# Search + Filters
# ----------------------------
with st.expander("🔎 Search & Filters", expanded=True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        q = st.text_input("Search (name/email/phone)", placeholder="e.g. john, gmail, 07...")
    with col2:
        trade = st.selectbox("Trade", ["All", "Plumber", "Electrician", "Handyman"])
    with col3:
        location = st.text_input("Location", placeholder="e.g. Bradford, Leeds")
    with col4:
        status_filter = st.selectbox(
            "Approval",
            ["All", "Approved", "Pending"]
        )

    col5, col6, col7 = st.columns(3)
    with col5:
        active_filter = st.selectbox("Active", ["All", "Active", "Inactive"])
    with col6:
        sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Business Name"])
    with col7:
        refresh = st.button("🔄 Refresh list")

# ----------------------------
# Load artisans based on filters
# ----------------------------
where = []
params = []

if q.strip():
    where.append("(business_name LIKE ? OR email LIKE ? OR phone LIKE ?)")
    like = f"%{q.strip()}%"
    params.extend([like, like, like])

if trade != "All":
    where.append("trade = ?")
    params.append(trade)

if location.strip():
    where.append("location = ?")
    params.append(location.strip().title())

if status_filter == "Approved":
    where.append("approved = 1")
elif status_filter == "Pending":
    where.append("approved = 0")

if active_filter == "Active":
    where.append("active = 1")
elif active_filter == "Inactive":
    where.append("active = 0")

where_sql = "WHERE " + " AND ".join(where) if where else ""

order_sql = "ORDER BY created_at DESC"
if sort_by == "Oldest":
    order_sql = "ORDER BY created_at ASC"
elif sort_by == "Business Name":
    order_sql = "ORDER BY business_name ASC"

query = f"""
SELECT artisan_id, business_name, email, phone, trade, location, approved, active, created_at
FROM artisans
{where_sql}
{order_sql}
"""

conn = get_connection()
df = pd.read_sql(query, conn, params=params)
conn.close()

st.subheader("📋 Registered Artisans")

if df.empty:
    st.info("No artisans match your filters.")
    st.stop()

st.caption(f"Showing {len(df)} artisan(s)")

# ----------------------------
# Render table + row buttons
# ----------------------------
# Show a clean view first
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("⚙️ Actions (Soft Delete / Restore)")

st.info("Soft delete = set active=0. Restore = set active=1. This keeps job history intact.")

for _, a in df.iterrows():
    left, mid, right = st.columns([6, 2, 2])

    with left:
        st.write(
            f"**#{a.artisan_id}** — {a.business_name} | {a.trade} | {a.location} "
            f"| {'✅ Approved' if a.approved else '🕒 Pending'} "
            f"| {'🟢 Active' if a.active else '🔴 Inactive'}"
        )
        st.caption(f"{a.email} | {a.phone or 'No phone'} | Created: {a.created_at}")

    with mid:
        if a.active == 1:
            if st.button("🗑 Deactivate", key=f"deact_{a.artisan_id}"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("UPDATE artisans SET active = 0 WHERE artisan_id = ?", (int(a.artisan_id),))
                conn.commit()
                conn.close()
                st.success(f"Deactivated: {a.business_name}")
                st.rerun()
        else:
            if st.button("♻️ Restore", key=f"restore_{a.artisan_id}"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("UPDATE artisans SET active = 1 WHERE artisan_id = ?", (int(a.artisan_id),))
                conn.commit()
                conn.close()
                st.success(f"Restored: {a.business_name}")
                st.rerun()

    with right:
        # Optional: HARD delete (dangerous) – only if you really want it
        with st.popover("⚠️ Hard Delete"):
            st.warning("This permanently deletes the artisan record.")
            confirm = st.checkbox("I understand", key=f"hard_confirm_{a.artisan_id}")
            if st.button("❌ Delete Permanently", key=f"hard_{a.artisan_id}", disabled=not confirm):
                conn = get_connection()
                c = conn.cursor()
                c.execute("DELETE FROM artisans WHERE artisan_id = ?", (int(a.artisan_id),))
                conn.commit()
                conn.close()
                st.success(f"Deleted permanently: {a.business_name}")
                st.rerun()
