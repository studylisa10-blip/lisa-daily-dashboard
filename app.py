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
    margin-bottom: 15px;
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
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 Lisa's Daily Pulse")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Football",
        "News",
        "AI News",
        "Learning"
    ]
)

# --------------------------------------------------
# FUNCTIONS
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


def get_bbc_news():

    try:

        feed = feedparser.parse(
            "https://feeds.bbci.co.uk/news/rss.xml"
        )

        return feed.entries[:5]

    except:

        return []


def get_football_news():

    try:

        feed = feedparser.parse(
            "https://feeds.bbci.co.uk/sport/football/rss.xml"
        )

        return feed.entries[:10]

    except:

        return []


def get_ai_news():

    try:

        feed = feedparser.parse(
            "https://www.artificialintelligence-news.com/feed/"
        )

        return feed.entries[:10]

    except:

        return []

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

weather = get_weather()

mens_fixture = get_mens_fixture()

bbc_news = get_bbc_news()

football_news = get_football_news()

ai_news = get_ai_news()

# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "Home":

    st.title("🚀 Lisa's Daily Pulse")

    st.caption(
        datetime.now().strftime("%A %d %B %Y")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
        <div class="card">
        <h3>🌦 Worthing Weather</h3>
        <h1>{weather}°C</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        if mens_fixture:

            st.markdown(f"""
            <div class="card">
            <h3>⚽ Manchester United Men</h3>

            <b>
            {mens_fixture['strHomeTeam']}
            vs
            {mens_fixture['strAwayTeam']}
            </b>

            <br><br>

            {mens_fixture['dateEvent']}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("☕ Morning Briefing")

    st.info(
        f"""
Good morning Lisa.

Worthing temperature: {weather}°C.

Check Football News and AI News for today's updates.
"""
    )

# --------------------------------------------------
# FOOTBALL PAGE
# --------------------------------------------------

elif page == "Football":

    st.title("⚽ Football News")

    for article in football_news:

        st.markdown(f"""
        <div class="news">
        <b>{article.title}</b>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# NEWS PAGE
# --------------------------------------------------

elif page == "News":

    st.title("📰 BBC Headlines")

    for article in bbc_news:

        st.markdown(f"""
        <div class="news">
        <b>{article.title}</b>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# AI NEWS PAGE
# --------------------------------------------------

elif page == "AI News":

    st.title("🤖 AI News")

    for article in ai_news:

        st.markdown(f"""
        <div class="news">
        <b>{article.title}</b>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# LEARNING
# --------------------------------------------------

elif page == "Learning":

    st.title("📚 Learning")

    st.write("• Streamlit")
    st.write("• Python")
    st.write("• AI")
    st.write("• Power BI")
    st.write("• Databricks")
    st.write("• SQL")

st.sidebar.success("✅ Dashboard Live")
