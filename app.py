import streamlit as st
import numpy as np
import joblib
import requests

# Load model and encoders
model = joblib.load('model.pkl')
le_type = joblib.load('type_encoder.pkl')
le_failure = joblib.load('failure_encoder.pkl')

st.set_page_config(page_title="Machine Failure Type Predictor")

st.title("🔧 Machine Failure Type Predictor")

# Get email from query parameter
email = st.query_params.get("email", "unknown@example.com")

# Input fields
type_label = st.selectbox("Type", le_type.classes_)
air_temp = st.number_input("Air Temperature [K]", min_value=270.0, max_value=400.0)
process_temp = st.number_input("Process Temperature [K]", min_value=270.0, max_value=500.0)
rpm = st.number_input("Rotational Speed [RPM]", min_value=0.0, max_value=5000.0)
torque = st.number_input("Torque [Nm]", min_value=0.0, max_value=100.0)
wear = st.number_input("Tool Wear [min]", min_value=0.0, max_value=250.0)

# Predict and log
if st.button("Predict Failure Type"):
    type_encoded = le_type.transform([type_label])[0]
    features = np.array([[type_encoded, air_temp, process_temp, rpm, torque, wear]])
    prediction = model.predict(features)[0]
    prediction_label = le_failure.inverse_transform([prediction])[0]

    st.success(f"🧠 Predicted Failure Type: **{prediction_label}**")

    # Log to backend
    try:
        response = requests.post("http://localhost:4000/api/history/log", json={
            "email": email,
            "prediction": prediction_label
        })
        if response.status_code == 201:
            st.info("✅ Prediction logged.")
        else:
            st.warning("⚠️ Failed to log prediction.")
    except Exception as e:
        st.error(f"Logging failed: {e}")
