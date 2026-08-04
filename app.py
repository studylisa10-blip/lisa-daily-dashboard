import streamlit as st
import requests
import feedparser
from datetime import datetime

# --------------------------------------------------
# PAGE
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
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
}

.news {
    background-color: #111827;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# WEATHER
# --------------------------------------------------

def get_weather():

    try:

        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=50.817"
            "&longitude=-0.375"
            "&current=temperature_2m"
        )

        response = requests.get(url, timeout=10)

        data = response.json()

        if "current" in data:
            return data["current"]["temperature_2m"]

        return "N/A"

    except:
        return "N/A"

# --------------------------------------------------
# MEN
# --------------------------------------------------

def get_mens_fixture():

    try:

        url = (
            "https://www.thesportsdb.com/api/v1/json/123/"
            "eventsnext.php?id=133612"
        )

        data = requests.get(url, timeout=10).json()

        fixtures = data.get("events", [])

        if fixtures:
            return fixtures[0]

        return None

    except:
        return None

# --------------------------------------------------
# WOMEN
# --------------------------------------------------

def get_womens_fixture():

    return None

# --------------------------------------------------
# NEWS
# --------------------------------------------------

def get_headlines():

    try:

        feed = feedparser.parse(
            "https://feeds.bbci.co.uk/news/rss.xml"
        )

        return feed.entries[:5]

    except:

        return []

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

weather = get_weather()

mens_fixture = get_mens_fixture()

headlines = get_headlines()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚀 Lisa's Daily Pulse")

st.caption(
    datetime.now().strftime("%A %d %B %Y")
)

# --------------------------------------------------
# CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="card">
    <h3>🌦 Weather</h3>
    <h1>{weather}°C</h1>
    <p>Worthing</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    if mens_fixture:

        st.markdown(f"""
        <div class="card">
        <h3>⚽ Man United Men</h3>

        <b>
        {mens_fixture['strHomeTeam']}
        vs
        {mens_fixture['strAwayTeam']}
        </b>

        <br><br>

        {mens_fixture['dateEvent']}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
        <h3>⚽ Man United Men</h3>
        No fixture available
        </div>
        """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">
    <h3>⚽ Man United Women</h3>
    Coming next update 👌
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# BRIEFING
# --------------------------------------------------

st.divider()

st.subheader("☕ Morning Briefing")

st.info(
    f"""
Good morning Lisa.

Current temperature:
{weather}°C

BBC Headlines are listed below.
"""
)

# --------------------------------------------------
# NEWS
# --------------------------------------------------

st.divider()

st.subheader("📰 BBC Headlines")

for article in headlines:

    st.markdown(f"""
    <div class="news">
    <b>{article.title}</b>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.success(
    "✅ Weather | ✅ Men's Fixtures | ✅ BBC Headlines"
)
