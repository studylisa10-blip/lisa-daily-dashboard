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


# Manchester United Fixtures

def get_fixtures():

    url = "https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id=133612"

    data = requests.get(url).json()

    return data.get("events", [])


# PAGE

st.title("🚀 Lisa's Daily Pulse")

col1, col2 = st.columns(2)

with col1:

    temp = get_weather()

    st.metric(
        "Worthing Temperature",
        f"{temp} °C"
    )

with col2:

    st.subheader("⚽ Manchester United")

    fixtures = get_fixtures()

    if fixtures:

        fixture = fixtures[0]

        st.write(
            f"{fixture['strHomeTeam']} vs {fixture['strAwayTeam']}"
        )

        st.write(
            fixture['dateEvent']
        )

    else:

        st.write(
            "No fixture returned"
        )

st.success("✅ Weather + Football loaded")
