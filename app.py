import streamlit as st
import requests
import feedparser
from datetime import datetime

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# FUNCTIONS
# -----------------------------

def get_weather():

    return 19

def get_mens_fixture():

    return {
        "home": "Manchester United",
        "away": "Paris Saint-Germain",
        "date": "2026-08-08",
        "time": "15:00"
    }

def get_womens_fixture():

    return {
        "home": "London City",
        "away": "Manchester United Women",
        "date": "2026-09-04",
        "time": "11:00"
    }

def get_headlines():

    try:

        feed = feedparser.parse(
            "https://feeds.bbci.co.uk/news/rss.xml"
        )

        return feed.entries[:5]

    except:

        return []

# -----------------------------
# LOAD DATA
# -----------------------------

weather = get_weather()

mens = get_mens_fixture()

womens = get_womens_fixture()

headlines = get_headlines()

# -----------------------------
# SIDEBAR
# -----------------------------

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

# -----------------------------
# HOME
# -----------------------------

if page == "Home":

    st.title("🚀 Lisa's Daily Pulse")

    st.caption(
        datetime.now().strftime("%A %d %B %Y")
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🌦 Weather",
            f"{weather}°C"
        )

    with col2:

        st.subheader(
            "⚽ Manchester United Men"
        )

        st.write(
            f"{mens['home']} vs {mens['away']}"
        )

        st.write(
            f"📅 {mens['date']}"
        )

        st.write(
            f"🕒 {mens['time']}"
        )

    with col3:

        st.subheader(
            "⚽ Manchester United Women"
        )

        st.write(
            f"{womens['home']} vs {womens['away']}"
        )

        st.write(
            f"📅 {womens['date']}"
        )

        st.write(
            f"🕒 {womens['time']}"
        )

    st.divider()

    st.subheader("☕ Morning Briefing")

    st.info(
        f"""
Good morning Lisa.

Current temperature in Worthing: {weather}°C

Next Manchester United men's fixture:
{mens['home']} vs {mens['away']}

Next Manchester United women's fixture:
{womens['home']} vs {womens['away']}
"""
    )

elif page == "Football":

    st.title("⚽ Football")

    st.write("Manchester United Men")
    st.write(f"{mens['home']} vs {mens['away']}")
    st.write(f"📅 {mens['date']}")
    st.write(f"🕒 {mens['time']}")

    st.divider()

    st.write("Manchester United Women")
    st.write(f"{womens['home']} vs {womens['away']}")
    st.write(f"📅 {womens['date']}")
    st.write(f"🕒 {womens['time']}")

elif page == "News":

    st.title("📰 BBC Headlines")

    for article in headlines:

        st.write(
            article.title
        )

elif page == "Learning":

    st.title("📚 Learning")

    st.write("• Streamlit")
    st.write("• Python")
    st.write("• AI")
    st.write("• Power BI")
    st.write("• Databricks")
