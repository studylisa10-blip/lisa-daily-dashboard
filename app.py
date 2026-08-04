import streamlit as st
import requests

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# Weather

def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=50.817"
        "&longitude=-0.375"
        "&current=temperature_2m"
    )

    data = requests.get(url).json()

    return data["current"]["temperature_2m"]

# Page

st.title("🚀 Lisa's Daily Pulse")

temp = get_weather()

st.metric(
    "Worthing Temperature",
    f"{temp} °C"
)

st.success("✅ Open-Meteo is working")
