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
# STYLING
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

.big_title {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

.subtitle {
    font-size: 18px;
    color: #94A3B8;
    margin-bottom: 25px;
}

.card {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
}

.news_card {
    background-color: #111827;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 5px solid #38BDF8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# WEATHER
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

# --------------------------------------------------
# MAN UTD MEN
# --------------------------------------------------

def get_mens_fixture():

    url = (
        "https://www.thesportsdb.com/api/v1/json/123/"
        "eventsnext.php?id=133612"
    )

    data = requests.get(url).json()

    fixtures = data.get("events", [])

    if fixtures:
        return fixtures[0]

    return None

# --------------------------------------------------
# MAN UTD WOMEN
# --------------------------------------------------

def get_womens_fixture():

    search_url = (
        "https://www.thesportsdb.com/api/v1/json/123/"
        "searchteams.php?t=Manchester%20United%20Women"
    )

    search_data = requests.get(search_url).json()

    teams = search_data.get("teams", [])

    if not teams:
        return None

    team_id = teams[0]["idTeam"]

    fixture_url = (
        f"https://www.thesportsdb.com/api/v1/json/123/"
        f"eventsnext.php?id={team_id}"
    )

    fixture_data = requests.get(fixture_url).json()

    fixtures = fixture_data.get("events", [])

    if fixtures:
        return fixtures[0]

    return None

# --------------------------------------------------
# BBC NEWS
# --------------------------------------------------

def get_headlines():

    feed = feedparser.parse(
        "https://feeds.bbci.co.uk/news/rss.xml"
    )

    return feed.entries[:5]

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

weather = get_weather()

mens_fixture = get_mens_fixture()

womens_fixture = get_womens_fixture()

headlines = get_headlines()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="big_title">🚀 Lisa\'s Daily Pulse</div>',
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

col1, col2, col3 = st.columns(3)

# WEATHER

with col1:

    st.markdown(f"""
    <div class='card'>
        <h3>🌦 Weather</h3>
        <h1>{weather}°C</h1>
        <p>Worthing</p>
    </div>
    """, unsafe_allow_html=True)

# MEN

with col2:

    if mens_fixture:

        st.markdown(f"""
        <div class='card'>
            <h3>⚽ United Men</h3>

            <b>
            {mens_fixture['strHomeTeam']}
            vs
            {mens_fixture['strAwayTeam']}
            </b>

            <br><br>

            {mens_fixture['dateEvent']}
        </div>
        """, unsafe_allow_html=True)

# WOMEN

with col3:

    if womens_fixture:

        st.markdown(f"""
        <div class='card'>
            <h3>⚽ United Women</h3>

            <b>
            {womens_fixture['strHomeTeam']}
            vs
            {womens_fixture['strAwayTeam']}
            </b>

            <br><br>

            {womens_fixture['dateEvent']}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class='card'>
            <h3>⚽ United Women</h3>
            No upcoming fixture found
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# BRIEFING
# --------------------------------------------------

st.divider()

st.subheader("☕ Morning Briefing")

mens_text = "Fixture unavailable"

if mens_fixture:

    mens_text = (
        f"{mens_fixture['strHomeTeam']} vs "
        f"{mens_fixture['strAwayTeam']}"
    )

st.info(
    f"""
Good morning Lisa.

Worthing is currently {weather}°C.

Next Manchester United men's fixture:

{mens_text}

Top BBC headlines are listed below.
"""
)

# --------------------------------------------------
# NEWS
# --------------------------------------------------

st.divider()

st.subheader("📰 BBC Headlines")

for article in headlines:

    st.markdown(f"""
    <div class='news_card'>
        <b>{article.title}</b>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOCUS
# --------------------------------------------------

st.divider()

st.subheader("🎯 Today's Focus")

st.write("• Check Manchester United fixtures")
st.write("• Catch up on the news")
st.write("• Keep improving Lisa's Daily Pulse")
st.write("• Add more personalised sections")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.success(
    "✅ Weather Loaded | ✅ Men's Fixtures | ✅ Women's Fixtures | ✅ BBC Headlines"
)
