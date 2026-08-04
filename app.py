import streamlit as st
import requests
import feedparser
from datetime import datetime

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# STYLE
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

.card {
    background-color: #1e293b;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 15px;
    min-height: 210px;
}

.news {
    background-color: #111827;
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 5px solid #38bdf8;
}

.small_text {
    color: #cbd5e1;
    font-size: 14px;
}

.big_metric {
    font-size: 42px;
    font-weight: 800;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 Lisa's Daily Pulse")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Football",
        "News",
        "Learning"
    ]
)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def clean_time(time_value):

    if not time_value:
        return "TBC"

    time_value = str(time_value)

    if len(time_value) >= 5:
        return time_value[:5]

    return time_value


def fixture_title(fixture):

    if not fixture:
        return "No fixture available"

    return f"{fixture.get('strHomeTeam', 'TBC')} vs {fixture.get('strAwayTeam', 'TBC')}"


def fixture_date(fixture):

    if not fixture:
        return "Date TBC"

    return fixture.get("dateEvent") or "Date TBC"


def fixture_time(fixture):

    if not fixture:
        return "Time TBC"

    return clean_time(fixture.get("strTime"))


# --------------------------------------------------
# WEATHER
# --------------------------------------------------

def get_weather():

    try:

        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": 50.817,
            "longitude": -0.375,
            "current": "temperature_2m",
            "timezone": "Europe/London"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        current = data.get("current", {})

        temp = current.get("temperature_2m")

        if temp is not None:
            return temp

    except:
        pass

    try:

        fallback_url = "https://api.open-meteo.com/v1/forecast"

        fallback_params = {
            "latitude": 50.817,
            "longitude": -0.375,
            "current_weather": "true",
            "timezone": "Europe/London"
        }

        fallback_response = requests.get(
            fallback_url,
            params=fallback_params,
            timeout=10
        )

        fallback_data = fallback_response.json()

        current_weather = fallback_data.get("current_weather", {})

        temp = current_weather.get("temperature")

        if temp is not None:
  
