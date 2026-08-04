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
            return temp

    except:
        pass

    return "N/A"


# --------------------------------------------------
# MEN FIXTURES
# --------------------------------------------------

def get_mens_fixtures():

    try:

        url = (
            "https://www.thesportsdb.com/api/v1/json/123/"
            "eventsnext.php?id=133612"
        )

        data = requests.get(
            url,
            timeout=10
        ).json()

        fixtures = data.get("events", [])

        if fixtures:
            return fixtures[:3]

        return []

    except:

        return []


def get_mens_fixture():

    fixtures = get_mens_fixtures()

    if fixtures:
        return fixtures[0]

    return None


# --------------------------------------------------
# WOMEN FIXTURES
# --------------------------------------------------

def get_womens_fixtures_from_api():

    try:

        search_url = (
            "https://www.thesportsdb.com/api/v1/json/123/"
            "searchteams.php?t=Manchester%20United%20Women"
        )

        search_data = requests.get(
            search_url,
            timeout=10
        ).json()

        teams = search_data.get("teams", [])

        if not teams:
            return []

        team_id = teams[0].get("idTeam")

        if not team_id:
            return []

        fixture_url = (
            "https://www.thesportsdb.com/api/v1/json/123/"
            f"eventsnext.php?id={team_id}"
        )

        fixture_data = requests.get(
            fixture_url,
            timeout=10
        ).json()

        fixtures = fixture_data.get("events", [])

        if fixtures:
            return fixtures[:3]

        return []

    except:

        return []


def get_womens_fixtures_fallback():

    return [
        {
            "strHomeTeam": "London City",
            "strAwayTeam": "Manchester United Women",
            "dateEvent": "2026-09-04",
            "strTime": "11:00",
            "strLeague": "Women's Super League",
            "strVenue": "Copperjax Community Stadium, London"
        },
        {
            "strHomeTeam": "Manchester United Women",
            "strAwayTeam": "Chelsea Women",
            "dateEvent": "2026-09-13",
            "strTime": "04:00",
            "strLeague": "Women's Super League",
            "strVenue": "Progress with Unity Stadium, Leigh"
        },
        {
            "strHomeTeam": "Arsenal Women",
            "strAwayTeam": "Manchester United Women",
            "dateEvent": "2026-09-19",
            "strTime": "09:30",
            "strLeague": "Women's Super League",
            "strVenue": "Emirates Stadium, London"
        }
    ]


def get_womens_fixtures():

    api_fixtures = get_womens_fixtures_from_api()

    if api_fixtures:
        return api_fixtures

    return get_womens_fixtures_fallback()


def get_womens_fixture():

    fixtures = get_womens_fixtures()

    if fixtures:
        return fixtures[0]

    return None


# --------------------------------------------------
# BBC NEWS
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
mens_fixtures = get_mens_fixtures()

womens_fixture = get_womens_fixture()
womens_fixtures = get_womens_fixtures()

headlines = get_headlines()

if weather == "N/A":
    weather_display = "N/A"
else:
    weather_display = f"{weather}°C"


# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "Home":

    st.title("🚀 Lisa's Daily Pulse")

    st.caption(
        datetime.now().strftime("%A %d %B %Y")
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="card">
            <h3>🌦 Weather</h3>
            <div class="big_metric">{weather_display}</div>
            <p>Worthing</p>
            <p class="small_text">Live temperature from Open-Meteo</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        if mens_fixture:

            st.markdown(f"""
            <div class="card">
                <h3>⚽ Manchester United Men</h3>

                <b>{fixture_title(mens_fixture)}</b>

                <br><br>

                📅 {fixture_date(mens_fixture)}

                <br><br>

                🕒 {fixture_time(mens_fixture)}
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="card">
                <h3>⚽ Manchester United Men</h3>
                No fixture available
            </div>
            """, unsafe_allow_html=True)

    with col3:

        if womens_fixture:

            st.markdown(f"""
            <div class="card">
                <h3>⚽ Manchester United Women</h3>

                <b>{fixture_title(womens_fixture)}</b>

                <br><br>

                📅 {fixture_date(womens_fixture)}

                <br><br>

                🕒 {fixture_time(womens_fixture)}
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="card">
                <h3>⚽ Manchester United Women</h3>
                No fixture available
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("☕ Morning Briefing")

    men_text = fixture_title(mens_fixture)
    women_text = fixture_title(womens_fixture)

    st.info(
        f"""
Good morning Lisa.

Current temperature in Worthing: {weather_display}

Next Manchester United men's fixture:
{men_text}

Next Manchester United women's fixture:
{women_text}

Check the News page for today's BBC headlines.
"""
    )


# --------------------------------------------------
# FOOTBALL PAGE
# --------------------------------------------------

elif page == "Football":

    st.title("⚽ Football")

    st.subheader("Manchester United Men")

    if mens_fixtures:

        for fixture in mens_fixtures:

            st.markdown(f"""
            <div class="card">
                <h3>{fixture_title(fixture)}</h3>
                <p>📅 {fixture_date(fixture)}</p>
                <p>🕒 {fixture_time(fixture)}</p>
                <p class="small_text">{fixture.get("strLeague", "Competition TBC")}</p>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.warning("No men's fixtures returned.")

    st.divider()

    st.subheader("Manchester United Women")

    if womens_fixtures:

        for fixture in womens_fixtures:

            st.markdown(f"""
            <div class="card">
                <h3>{fixture_title(fixture)}</h3>
                <p>📅 {fixture_date(fixture)}</p>
                <p>🕒 {fixture_time(fixture)}</p>
                <p class="small_text">{fixture.get("strLeague", "Competition TBC")}</p>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.warning("No women's fixtures returned.")


# --------------------------------------------------
# NEWS
# --------------------------------------------------

elif page == "News":

    st.title("📰 BBC Headlines")

    if headlines:

        for article in headlines:

            st.markdown(
                f"""
                <div class="news">
                    <b>{article.title}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning("No BBC headlines returned.")


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


# --------------------------------------------------
# STATUS
# --------------------------------------------------

st.sidebar.success("✅ Dashboard Live")
