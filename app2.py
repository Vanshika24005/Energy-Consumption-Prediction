import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Energy Consumption Predictor", layout="centered")

# Title
st.title("⚙️ Machine Energy Consumption Predictor")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("energy_model.pkl")

model = load_model()

# Load dataset for preview (optional)
@st.cache_data
def load_data():
    return pd.read_csv("machine_energy_consumption_dataset.csv")

df = load_data()

# Show dataset
st.subheader("📊 Sample Dataset")
st.write(df.head())

# Sidebar inputs
st.sidebar.header("🛠️ Input Parameters")

temperature = st.sidebar.slider("Temperature (°C)", 50.0, 100.0, 75.0)
vibration = st.sidebar.slider("Vibration (Hz)", 15.0, 50.0, 30.0)
pressure = st.sidebar.slider("Pressure (bar)", 2.0, 7.0, 4.5)
runtime = st.sidebar.slider("RunTime Hours", 300.0, 1200.0, 800.0)
humidity = st.sidebar.slider("Humidity (%)", 20.0, 70.0, 45.0)

input_data = pd.DataFrame({
    "Temperature (°C)": [temperature],
    "Vibration (Hz)": [vibration],
    "Pressure (bar)": [pressure],
    "RunTimeHours": [runtime],
    "Humidity (%)": [humidity]
})

# Predict button
if st.sidebar.button("🔍 Predict Energy Consumption"):
    prediction = model.predict(input_data)[0]
    st.subheader("🔋 Predicted Energy Consumption")
    st.success(f"Estimated Usage: **{prediction:.2f} kWh**")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Sankalp • Model: Random Forest (loaded from .pkl)")
