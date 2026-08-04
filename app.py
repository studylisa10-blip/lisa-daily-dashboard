import streamlit as st
import requests
import feedparser
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

.title {
    font-size: 48px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #94A3B8;
    margin-bottom: 30px;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}

.news-card {
    background-color: #111827;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #38BDF8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def get_weather():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=50.817"
        "&longitude=-0.375"
        "&current=temperature_2m"
    )

    data = requests.get(url).json()

    return data["current"]["temperature_2m"]


def get_fixture():

    url = (
        "https://www.thesportsdb.com/api/v1/json/123/"
        "eventsnext.php?id=133612"
    )

    data = requests.get(url).json()

    fixtures = data.get("events", [])

    if fixtures:
        return fixtures[0]

    return None


def get_headlines():

    feed = feedparser.parse(
        "https://feeds.bbci.co.uk/news/rss.xml"
    )

    return feed.entries[:5]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🚀 Lisa\'s Daily Pulse</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal morning newspaper</div>',
    unsafe_allow_html=True
)

st.caption(
    datetime.now().strftime("%A %d %B %Y")
)

# --------------------------------------------------
# TOP CARDS
# --------------------------------------------------

weather = get_weather()
fixture = get_fixture()

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div class="card">
        <h3>🌦 Worthing Weather</h3>
        <h1>{weather}°C</h1>
        <p>Live Open-Meteo weather</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    if fixture:

        st.markdown(f"""
        <div class="card">
            <h3>⚽ Manchester United Men</h3>
            <h2>
            {fixture['strHomeTeam']} vs
            {fixture['strAwayTeam']}
            </h2>
            <p>{fixture['dateEvent']}</p>
        </div>
        """, unsafe_allow_html=True)

        fixture_text = (
            f"{fixture['strHomeTeam']} vs "
            f"{fixture['strAwayTeam']}"
        )

    else:

        fixture_text = "Fixture unavailable"

        st.markdown("""
        <div class="card">
            <h3>⚽ Manchester United Men</h3>
            <p>No fixture found</p>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# BRIEFING
# --------------------------------------------------

st.subheader("☕ Morning Briefing")

st.info(
    f"""
Welcome back Lisa.

The current temperature in Worthing is {weather}°C.

Your next Manchester United fixture is:

{fixture_text}

Below are today's BBC headlines.
"""
)

# --------------------------------------------------
# NEWS
# --------------------------------------------------

st.subheader("📰 BBC Headlines")

headlines = get_headlines()

for article in headlines:

    st.markdown(f"""
    <div class="news-card">
        <b>{article.title}</b>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# TODAY
# --------------------------------------------------

st.subheader("🎯 Today's Focus")

st.write("• Check the latest headlines")
st.write("• Keep building Lisa's Daily Pulse")
st.write("• Add Manchester United Women fixtures")
st.write("• Add AI news")
st.write("• Make the dashboard even cooler")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.success(
    "✅ Weather | ✅ Football | ✅ BBC News"
)
