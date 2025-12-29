
import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(layout="centered")

# Background color
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e3f2fd;  /* Soft sky blue */
}
</style>
""", unsafe_allow_html=True)

# Email credentials (use AWS Secrets Manager in production)
EMAIL_ADDRESS = "einstsoft7@gmail.com"      # TODO: move to secrets
EMAIL_PASSWORD = "ujfwfxnlmvyyjwxu"         # TODO: move to secrets

# Staff emails dictionary
PeelM_STAFF_EMAILS = {
    "Ejike": "einstpersonnelmanagement@gmail.com",
    "Ikenna": "igweikenna27@gmail.com",
    "David": "epms371@gmail.com",
    "Eli": "chukuejike@outlook.com",

}
ComSt_STAFF_EMAILS = {
    "Laura": "lauramack810@gmail.com",
    "James": "jamesonicha1@gmail.com",
    "Chuku": "ejikechuku@gmail.com",
    "Amal": "amals@ubu.me.uk",
    "Benedict": "chukwuejyk@yahoo.com"
}
ElRoad_STAFF_EMAILS = {
    "Chinwe": "chinweqorji@gmail.com",
    "Esther": "nwaniestha@gmail.com",
    "Uzor": "uzoamakao@gmail.com",
    "Chukuwuma": "chukwumao@oef.org.ng",
    
}

# Map services to the correct staff dict
SERVICE_TO_STAFF = {
    "Peel Mill": PeelM_STAFF_EMAILS,
    "Commercial Street": ComSt_STAFF_EMAILS,
    "Elland Road": ElRoad_STAFF_EMAILS,
}

# Users for login
USERS = {'ejyk': '1234567', 'chinwe': 'passTest', 'ulink': 'service'}

# Initialize session state safely
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Email sending function
def send_email(to, subject, message):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to
        msg.set_content(message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        st.success(f"Email sent to {to}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Streamlit UI
st.title("UBU Staff Job Assignment Portal")

# Login Section
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in USERS and USERS[username] == password:
        st.session_state["logged_in"] = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password")

# Show staff selection only if logged in
if st.session_state.get("logged_in"):
    st.subheader("Job Details")

    client_name = st.text_input("Client Name")
    client_address = st.text_input("Client Address")

    # Let user choose service so we know which staff list to use
    service = st.selectbox("Service / Location", list(SERVICE_TO_STAFF.keys()))
    STAFF_EMAILS = SERVICE_TO_STAFF[service]

    
    staff_names = st.multiselect("Select Staff", list(STAFF_EMAILS.keys()))
    date = st.text_input("Date (DD-MM-YYYY)")
    start_time = st.text_input("Start Time (HH:MM)")
    end_time = st.text_input("End Time (HH:MM)")

    if st.button("Send Email"):
         if client_name and client_address and staff_names and date and start_time and end_time:
           for staff_name in staff_names:
               message = (
                  f"Hi {staff_name},\n\n"
                  f"We need you to cover a shift.\n"
                  f"Client: {client_name}\n"
                  f"Address: {client_address}\n"
                  f"Date: {date}\n"
                  f"Start: {start_time}\n"
                  f"End: {end_time}\n\n"
                  f"You can call {client_address} if you need more details."
               )
               send_email(STAFF_EMAILS[staff_name], "Shift Cover", message)
         else:
             st.error("Please fill all fields and select at least one staff member")
