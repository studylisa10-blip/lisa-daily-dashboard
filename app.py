import streamlit as st
import requests
import feedparser

st.set_page_config(
    st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b1120, #111827);
}

.big-title {
    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-bottom: 0px;
}

.sub-title {
    color: #94A3B8;
    font-size: 18px;
}

.card {
    background: linear-gradient(
        135deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.95)
    );
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.card-title {
    color: #38BDF8;
    font-size: 22px;
    font-weight: 700;
}

.card-value {
    color: white;
    font-size: 34px;
    font-weight: bold;
    margin-top: 10px;
}

.news-card {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #38BDF8;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)
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
# MAN UNITED FIXTURE
# --------------------------

def get_mens_fixture():

    url = "https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id=133612"

    data = requests.get(url).json()

    fixtures = data.get("events", [])

    if len(fixtures) > 0:
        return fixtures[0]

    return None

# --------------------------
# BBC NEWS
# --------------------------

def get_headlines():

    feed = feedparser.parse(
        "https://feeds.bbci.co.uk/news/rss.xml"
    )

    return feed.entries[:5]

# --------------------------
# PAGE
# --------------------------

st.title("🚀 Lisa's Daily Pulse")

col1, col2 = st.columns(2)

with col1:

    temp = get_weather()

    st.metric(
        label="🌦 Worthing Temperature",
        value=f"{temp} °C"
    )

with col2:

    st.subheader("⚽ Manchester United Men")

    fixture = get_mens_fixture()

    if fixture:

        fixture_text = (
            f"{fixture['strHomeTeam']} vs "
            f"{fixture['strAwayTeam']}"
        )

        st.write(fixture_text)

        st.write(
            fixture["dateEvent"]
        )

    else:

        fixture_text = "Fixture unavailable"

        st.write(fixture_text)

st.divider()

st.subheader("☕ Morning Briefing")

st.info(
    f"""
Good morning Lisa.

Current temperature in Worthing: {temp}°C

Next Manchester United fixture:
{fixture_text}

Top headlines are below.
"""
)

st.divider()

st.subheader("📰 BBC Headlines")

headlines = get_headlines()

for article in headlines:

    st.markdown(
        f"**{article.title}**"
    )

    st.caption(
        article.link
    )

st.divider()

st.subheader("🎯 Today's Focus")

st.write("• Check the latest Manchester United news")
st.write("• Read today's top headlines")
st.write("• Continue building Lisa's Daily Pulse")
st.write("• Learn one new AI skill")

st.success(
    "✅ Weather Loaded | ✅ Football Loaded | ✅ BBC Headlines Loaded"
)
