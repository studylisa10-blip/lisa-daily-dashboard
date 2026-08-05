
```python
import streamlit as st
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide",
)

UK_TIMEZONE = ZoneInfo("Europe/London")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 Lisa's Daily Pulse")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Football", "News", "Learning"],
)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def current_uk_date() -> str:
    """Return today's date in the UK timezone."""
    return datetime.now(UK_TIMEZONE).strftime("%A %d %B %Y")


# --------------------------------------------------
# WEATHER
# --------------------------------------------------

def get_weather() -> str:
    """
    Temporary fixed weather.

    This can be replaced with a live weather API later.
    """
    return "19°C"


# --------------------------------------------------
# FIXTURES
# --------------------------------------------------

mens_fixtures = [
    {
        "home": "Manchester United",
        "away": "Paris Saint-Germain",
        "date": "08 Aug 2026",
        "time": "17:00",
        "competition": "Club Friendly",
    },
    {
        "home": "Manchester United",
        "away": "Arsenal",
        "date": "15 Aug 2026",
        "time": "17:30",
        "competition": "Premier League",
    },
    {
        "home": "Tottenham",
        "away": "Manchester United",
        "date": "22 Aug 2026",
        "time": "16:30",
        "competition": "Premier League",
    },
]

womens_fixtures = [
    {
        "home": "London City",
        "away": "Manchester United Women",
        "date": "04 Sep 2026",
        "time": "12:00",
        "competition": "Women's Super League",
    },
    {
        "home": "Manchester United Women",
        "away": "Chelsea Women",
        "date": "13 Sep 2026",
        "time": "13:00",
        "competition": "Women's Super League",
    },
    {
        "home": "Arsenal Women",
        "away": "Manchester United Women",
        "date": "19 Sep 2026",
        "time": "10:30",
        "competition": "Women's Super League",
    },
]


# --------------------------------------------------
# BBC HEADLINES
# --------------------------------------------------

@st.cache_data(ttl=900)
def get_headlines() -> list:
    """Load BBC News RSS headlines and cache them for 15 minutes."""
    try:
        feed = feedparser.parse(
            "https://feeds.bbci.co.uk/news/rss.xml"
        )

        if getattr(feed, "bozo", False) and not feed.entries:
            return []

        return list(feed.entries[:5])

    except Exception:
        return []


# --------------------------------------------------
# DISPLAY COMPONENTS
# --------------------------------------------------

def show_fixture_card(title: str, fixture: dict) -> None:
    st.subheader(title)
    st.markdown(
        f"**{fixture['home']} vs {fixture['away']}**"
    )
    st.write(f"📅 {fixture['date']}")
    st.write(f"🕒 {fixture['time']}")
    st.caption(fixture["competition"])


def show_fixture_list(fixtures: list[dict]) -> None:
    for fixture in fixtures:
        st.markdown(
            f"### {fixture['home']} vs {fixture['away']}"
        )
        st.write(f"📅 {fixture['date']}")
        st.write(f"🕒 {fixture['time']}")
        st.caption(fixture["competition"])
        st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

weather = get_weather()
headlines = get_headlines()

next_mens_fixture = mens_fixtures[0]
next_womens_fixture = womens_fixtures[0]


# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "Home":
    st.title("🚀 Lisa's Daily Pulse")
    st.caption(current_uk_date())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌦 Worthing", weather)

    with col2:
        st.metric("🌦 Salisbury", "22°C")

    with col3:
        show_fixture_card(
            "⚽ Manchester United Men",
            next_mens_fixture,
        )

    with col4:
        show_fixture_card(
            "⚽ Manchester United Women",
            next_womens_fixture,
        )

    st.divider()
    st.subheader("☕ Morning Briefing")

    st.info(
        f"""
Good morning Lisa.

**Current temperature:** {weather}

**Next Manchester United men's fixture:**  
{next_mens_fixture['home']} vs {next_mens_fixture['away']}  
📅 {next_mens_fixture['date']} at {next_mens_fixture['time']}

**Next Manchester United women's fixture:**  
{next_womens_fixture['home']} vs {next_womens_fixture['away']}  
📅 {next_womens_fixture['date']} at {next_womens_fixture['time']}
"""
    )


# --------------------------------------------------
# FOOTBALL
# --------------------------------------------------

elif page == "Football":
    st.title("⚽ Football")

    men_tab, women_tab = st.tabs(
        ["Manchester United Men", "Manchester United Women"]
    )

    with men_tab:
        show_fixture_list(mens_fixtures)

    with women_tab:
        show_fixture_list(womens_fixtures)


# --------------------------------------------------
# NEWS
# --------------------------------------------------

elif page == "News":
    st.title("📰 BBC Headlines")

    if not headlines:
        st.warning(
            "BBC headlines could not be loaded. Please try again later."
        )

    for article in headlines:
        title = article.get("title", "Untitled article")
        link = article.get("link", "")

        if link:
            st.markdown(f"### [{title}]({link})")
        else:
            st.markdown(f"### {title}")

        summary = article.get("summary")
        if summary:
            st.caption(summary)

        st.divider()


# --------------------------------------------------
# LEARNING
# --------------------------------------------------

elif page == "Learning":
    st.title("📚 Learning")

    learning_topics = [
        "Streamlit",
        "Python",
        "AI",
        "SQL",
        "Power BI",
        "Databricks",
    ]

    for topic in learning_topics:
        st.checkbox(topic, key=f"learning_{topic}")


# --------------------------------------------------
# STATUS
# --------------------------------------------------

st.sidebar.divider()
st.sidebar.success("✅ Dashboard Live")
