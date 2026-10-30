# landing_register.py
import streamlit as st

# Capture referral code from URL
query_params = st.experimental_get_query_params()
ref_code = query_params.get("ref", [""])[0]

# Store referral code in session state for use in registration
st.session_state['ref_code'] = ref_code

# Redirect immediately to the registration page
st.markdown("""
<meta http-equiv="refresh" content="0; url=/Artisan_Register">
""", unsafe_allow_html=True)

st.write("Redirecting to registration page...")
