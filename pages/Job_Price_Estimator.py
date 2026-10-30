import streamlit as st
from services.pricing_service import train_model, predict_price

st.title("🔧 Job Price Estimator")

# Train model when page loads
train_model()

st.write("Enter job details to get an estimated price")

job_type = st.selectbox("Job Type", ["Plumber", "Electrician", "Cleaner", "Gas Engineer", "Handyman", "Hairdresser"])
location = st.text_input("Location", "Leeds")
labor_hours = st.number_input("Labour Hours", min_value=1, max_value=24, value=2)
materials_cost = st.number_input("Materials Cost (£)", min_value=0.0, value=20.0)

if st.button("Estimate Price"):
    result = predict_price(job_type, location, labor_hours, materials_cost)

    if result:
        lower, upper = result
        st.success(f"💰 Estimated Price Range: £{lower} - £{upper}")
        st.info("This estimate is based on recent similar jobs.")
    else:
        st.error("Model not ready. Please refresh the page.")
