import streamlit as st
import requests

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# --------------------------
# WEATHER
# --------------------------

def get_weather():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=50.817"
        "&longitude=-0.375"
        "&current=temperature_2m"
    )

    data = requests.get(url).json()

    return data["current"]["temperature_2m"]


# --------------------------
# MAN UNITED MEN FIXTURES
# --------------------------

def get_mens_fixture():

    url = "https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id=133612"

    data = requests.get(url).json()

    fixtures = data.get("events", [])

    if len(fixtures) > 0:
        return fixtures[0]

    return None


# --------------------------
# PAGE
# --------------------------

st.title("🚀 Lisa's Daily Pulse")

col1, col2 = st.columns(2)

# WEATHER

with col1:

    temp = get_weather()

    st.metric(
        label="🌦 Worthing Temperature",
        value=f"{temp} °C"
    )

# FOOTBALL

with col2:

    st.subheader("⚽ Manchester United Men")

    fixture = get_mens_fixture()

    if fixture:

        st.write(
            f"**{fixture['strHomeTeam']} vs {fixture['strAwayTeam']}**"
        )

        st.write(
            fixture["dateEvent"]
        )

    else:

        st.write(
            "No fixture returned"
        )

st.divider()

st.subheader("🤖 Gemini")

st.info(
    "Next step: connect your Gemini API key and generate a personalised morning briefing."
)

st.success(
    "✅ Weather working | ✅ Football working"
)
