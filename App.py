import streamlit as st

from database import (
    init_db,
    migrate_add_description,
    migrate_add_artisan_code,
    migrate_add_referrals
)

# 🔹 Run database setup
init_db()
migrate_add_description()
migrate_add_artisan_code()
migrate_add_referrals()


st.title("EPMS LTD 🛠")

# HERO
st.markdown("""
### Connecting Clients with Trusted Local Professionals 🤝

**Plumbing • Electrical • Handyman • Cleaning • Hairdressing**  
""")

st.info("Fast requests • Trusted professionals • Clear job updates", icon="✨")

st.divider()

# CTA SECTION
st.markdown("## Get started 👇")
st.markdown("Use the menu on the left, or choose an option below:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🙋 For Clients")
    st.markdown("""
- 📨 Submit a job request  
- 🔎 Track your job status  
""")
    st.page_link("pages/Client_Request.py", label="📨 Request a Service", use_container_width=True)
    # If your tracking page has a different name, update it here:
    st.page_link("pages/Client_Dashboard.py", label="🔎 Track My Job", use_container_width=True)

with col2:
    st.markdown("### 👷 For Artisans")
    st.markdown("""
- 🧾 Register to be approved  
- ✅ View and accept available jobs  
""")
    st.page_link("pages/Artisan_Register.py", label="🧾 Artisan Register", use_container_width=True)
    st.page_link("pages/Artisan_Accept.py", label="✅ View & Accept Jobs", use_container_width=True)

st.divider()

# HOW IT WORKS (your original guidance, formatted)
st.markdown("## How EPMS works ⚙️")
st.markdown("""
- 📝 **Clients** use **Client Request** to submit a request for skilled professionals.
- 🧰 **Artisans** use **Artisan Register** to sign up and get approved for jobs.
- ✅ Approved artisans can **view open jobs**, **accept jobs**, and move jobs forward.

""")

# POLICIES LINK
st.caption("📜 By using EPMS, you agree to our platform policies.")
st.page_link("pages/Artisan_platform_Legal_Policies.py", label="View Policies →")
