# services/pricing_service.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# Global variables
model = None
encoder_job = None
encoder_loc = None


# -------------------------------
# Sample data (temporary)
# -------------------------------
def load_sample_data():
    return pd.DataFrame([
        {'job_type':'Plumber', 'location':'Leeds', 'labor_hours':3, 'materials_cost':50, 'total_price':200},
        {'job_type':'Electrician', 'location':'Manchester', 'labor_hours':2, 'materials_cost':30, 'total_price':120},
        {'job_type':'Cleaner', 'location':'Leeds', 'labor_hours':1, 'materials_cost':10, 'total_price':50},
        {'job_type':'Plumber', 'location':'Leeds', 'labor_hours':4, 'materials_cost':70, 'total_price':260},
    ])


# -------------------------------
# Train model
# -------------------------------
def train_model():
    global model, encoder_job, encoder_loc

    data = load_sample_data()

    encoder_loc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoder_job = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    loc_encoded = encoder_loc.fit_transform(data[['location']])
    job_encoded = encoder_job.fit_transform(data[['job_type']])

    X = np.concatenate([
        loc_encoded,
        job_encoded,
        data[['labor_hours','materials_cost']].values
    ], axis=1)

    y = data['total_price']

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)


# -------------------------------
# Predict price
# -------------------------------
def predict_price(job_type, location, labor_hours, materials_cost):
    global model

    # Safety check
    if model is None:
        return None

    loc_enc = encoder_loc.transform([[location]])
    job_enc = encoder_job.transform([[job_type]])

    X_new = np.concatenate([
        loc_enc,
        job_enc,
        [[labor_hours, materials_cost]]
    ], axis=1)

    prediction = model.predict(X_new)[0]

    # Return range instead of single value
    lower = prediction * 0.9
    upper = prediction * 1.1

    return round(lower, 2), round(upper, 2)
