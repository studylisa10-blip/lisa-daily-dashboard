import streamlit as st
import requests
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

UK_TIMEZONE = ZoneInfo("Europe/London")
UTC_TIMEZONE = ZoneInfo("UTC")

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
# DATE AND TIME HELPERS
# --------------------------------------------------

def current_uk_date():

    return datetime.now(UK_TIMEZONE).strftime("%A %d %B %Y")


def get_weather():

    try:

        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 50.817,
                "longitude": -0.375,
                "current": "temperature_2m"
            },
            timeout=20
        )

        data = response.json()

        return str(
            data["current"]["temperature_2m"]
        ) + "°C"

    except Exception as e:

        return str(e)


def format_sportsdb_fixture(fixture):

    if not fixture:
        return {
            "home": "Fixture unavailable",
            "away": "",
            "date": "Date TBC",
            "time": "Time TBC",
            "competition": "Competition TBC"
        }

    home = fixture.get("strHomeTeam", "TBC")
    away = fixture.get("strAwayTeam", "TBC")
    date_value = fixture.get("dateEvent")
    time_value = fixture.get("strTime")
    competition = fixture.get("strLeague", "Competition TBC")

    date_display, time_display = convert_utc_to_uk(
        date_value,
        time_value
    )

    return {
        "home": home,
        "away": away,
        "date": date_display,
        "time": time_display,
        "competition": competition
    }


def format_manual_fixture(fixture):

    if not fixture:
        return {
            "home": "Fixture unavailable",
            "away": "",
            "date": "Date TBC",
            "time": "Time TBC",
            "competition": "Competition TBC"
        }

    date_display, time_display = convert_utc_to_uk(
        fixture.get("date"),
        fixture.get("time")
    )

    return {
        "home": fixture.get("home", "TBC"),
        "away": fixture.get("away", "TBC"),
        "date": date_display,
        "time": time_display,
        "competition": fixture.get("competition", "Competition TBC")
    }


# --------------------------------------------------
# WEATHER
# --------------------------------------------------

def get_weather():

    try:

        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 50.817,
                "longitude": -0.375,
                "current": "temperature_2m",
                "timezone": "Europe/London"
            },
            timeout=10
        )

        data = response.json()

        current = data.get("current", {})

        temp = current.get("temperature_2m")

        if temp is not None:
            return f"{round(float(temp), 1)}°C"

    except:
        pass

    return "Unavailable"


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
            formatted_fixtures = []

            for fixture in fixtures[:3]:
                formatted_fixtures.append(
                    format_sportsdb_fixture(fixture)
                )

            return formatted_fixtures

        return []

    except:

        return []


def get_womens_fixtures_fallback():

    fallback_fixtures = [
        {
            "home": "London City",
            "away": "Manchester United Women",
            "date": "2026-09-04",
            "time": "11:00",
            "competition": "Women's Super League"
        },
        {
            "home": "Manchester United Women",
            "away": "Chelsea Women",
            "date": "2026-09-13",
            "time": "04:00",
            "competition": "Women's Super League"
        },
        {
            "home": "Arsenal Women",
            "away": "Manchester United Women",
            "date": "2026-09-19",
            "time": "09:30",
            "competition": "Women's Super League"
        }
    ]

    formatted_fixtures = []

    for fixture in fallback_fixtures:
        formatted_fixtures.append(
            format_manual_fixture(fixture)
        )

    return formatted_fixtures


def get_womens_fixtures():

    api_fixtures = get_womens_fixtures_from_api()

    if api_fixtures:
        return api_fixtures

    return get_womens_fixtures_fallback()


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

raw_mens_fixtures = get_mens_fixtures()

mens_fixtures = []

for fixture in raw_mens_fixtures:
    mens_fixtures.append(
        format_sportsdb_fixture(fixture)
    )

womens_fixtures = get_womens_fixtures()

headlines = get_headlines()

next_mens_fixture = mens_fixtures[0] if mens_fixtures else None
next_womens_fixture = womens_fixtures[0] if womens_fixtures else None


# --------------------------------------------------
# DISPLAY HELPERS
# --------------------------------------------------

def show_fixture_card(title, fixture):

    st.subheader(title)

    if not fixture:

        st.warning("No fixture available")
        return

    st.write(
        f"{fixture['home']} vs {fixture['away']}"
    )

    st.write(
        f"📅 {fixture['date']}"
    )

    st.write(
        f"🕒 {fixture['time']}"
    )

    st.caption(
        fixture["competition"]
    )


def show_fixture_list(fixtures):

    if not fixtures:

        st.warning("No fixtures available")
        return

    for fixture in fixtures:

        st.write(
            f"### {fixture['home']} vs {fixture['away']}"
        )

        st.write(
            f"📅 {fixture['date']}"
        )

        st.write(
            f"🕒 {fixture['time']}"
        )

        st.caption(
            fixture["competition"]
        )

        st.divider()


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.title("🚀 Lisa's Daily Pulse")

    st.caption(
        current_uk_date()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("🌦 Worthing Weather")

        st.metric(
            label="Current Temperature",
            value=weather
        )

    with col2:

        show_fixture_card(
            "⚽ Manchester United Men",
            next_mens_fixture
        )

    with col3:

        show_fixture_card(
            "⚽ Manchester United Women",
            next_womens_fixture
        )

    st.divider()

    st.subheader("☕ Morning Briefing")

    if next_mens_fixture:
        men_text = (
            f"{next_mens_fixture['home']} vs "
            f"{next_mens_fixture['away']} on "
            f"{next_mens_fixture['date']} at "
            f"{next_mens_fixture['time']}"
        )
    else:
        men_text = "No men's fixture available"

    if next_womens_fixture:
        women_text = (
            f"{next_womens_fixture['home']} vs "
            f"{next_womens_fixture['away']} on "
            f"{next_womens_fixture['date']} at "
            f"{next_womens_fixture['time']}"
        )
    else:
        women_text = "No women's fixture available"

    st.info(
        f"""
Good morning Lisa.

Current temperature:
{weather}

Next Manchester United men's fixture:
{men_text}

Next Manchester United women's fixture:
{women_text}

Check today's headlines on the News page.
"""
    )


# --------------------------------------------------
# FOOTBALL PAGE
# --------------------------------------------------

elif page == "Football":

    st.title("⚽ Football")

    st.subheader("Manchester United Men")
    show_fixture_list(mens_fixtures)

    st.subheader("Manchester United Women")
    show_fixture_list(womens_fixtures)


# --------------------------------------------------
# NEWS PAGE
# --------------------------------------------------

elif page == "News":

    st.title("📰 BBC Headlines")

    if headlines:

        for article in headlines:

            st.write(
                f"### {article.title}"
            )

            if hasattr(article, "link"):
                st.caption(
                    article.link
                )

            st.divider()

    else:

        st.warning("No BBC headlines returned.")


# --------------------------------------------------
# LEARNING PAGE
# --------------------------------------------------

elif page == "Learning":

    st.title("📚 Learning")

    st.write("• Streamlit")
    st.write("• Python")
    st.write("• APIs")
    st.write("• AI")
    st.write("• Power BI")
    st.write("• Databricks")
    st.write("• SQL")


# --------------------------------------------------
# STATUS
# --------------------------------------------------

st.sidebar.success("✅ Dashboard Live")
