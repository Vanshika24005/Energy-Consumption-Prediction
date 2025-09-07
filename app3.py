import streamlit as st
import joblib
import numpy as np

# Set up page
st.set_page_config(page_title="🔧 Part Replacement Predictor", layout="centered")
st.title("🔧 Predict Which Machine Part Needs Replacement")

# Load model and label encoder
@st.cache_resource
def load_model():
    return joblib.load("part_replacement_multiclass_model.pkl")

@st.cache_resource
def load_encoder():
    return joblib.load("label_encoder.pkl")

model = load_model()
encoder = load_encoder()

# User inputs
temperature = st.number_input("🌡️ Temperature (°C)", value=75.0)
vibration = st.number_input("🌀 Vibration (mm/s)", value=0.5)
pressure = st.number_input("🔧 Pressure (PSI)", value=100.0)
runtime = st.number_input("⏱️ Runtime Hours", value=500.0)
age = st.number_input("📆 Part Age (Months)", value=12)

# Predict
if st.button("🔍 Predict"):
    input_features = np.array([[temperature, vibration, pressure, runtime, age]])
    prediction_encoded = model.predict(input_features)[0]
    prediction_label = encoder.inverse_transform([prediction_encoded])[0]

    st.subheader("🛠️ Prediction Result")
    if prediction_label == "None":
        st.success("✅ No part needs replacement right now.")
    else:
        st.error(f"⚠️ Suggested Replacement: **{prediction_label}**")

