import streamlit as st

st.set_page_config(page_title="Legal & Policies", layout="wide")
st.title("📜 Legal & Policies")

tab1, tab2, tab3, tab4 = st.tabs(["Terms of Use", "Privacy Policy", "Commission Policy", "Agreements"])

with tab1:
    st.markdown(open("legal/terms_of_use.md", "r", encoding="utf-8").read())

with tab2:
    st.markdown(open("legal/privacy_policy.md", "r", encoding="utf-8").read())

with tab3:
    st.markdown(open("legal/commission_policy.md", "r", encoding="utf-8").read())

with tab4:
    st.markdown(open("legal/artisan_agreement.md", "r", encoding="utf-8").read())
    st.markdown("---")
    st.markdown(open("legal/client_agreement.md", "r", encoding="utf-8").read())
