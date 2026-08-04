import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from google import genai
except Exception:
    genai = None


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

UK_TZ = ZoneInfo("Europe/London")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WORTHING_LATITUDE = 50.817
WORTHING_LONGITUDE = -0.375

THESPORTSDB_KEY = "123"
THESPORTSDB_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_KEY}"

MEN_TEAM_NAME = "Manchester United"
WOMEN_TEAM_NAME = "Manchester United Women"


# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .hero {
        background: linear-gradient(135deg, #18A0FB, #7B61FF);
        padding: 35px;
        border-radius: 24px;
        margin-bottom: 28px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
    }

    .hero h1 {
        color: white;
        font-size: 46px;
        margin-bottom: 8px;
    }

    .hero p {
        color: white;
        font-size: 17px;
    }

    .card {
        background: rgba(30, 41, 59, 0.92);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #334155;
        min-height: 230px;
        box-shadow: 0px 10px 24px rgba(0,0,0,0.22);
    }

    .card h3 {
        color: white;
        margin-bottom: 10px;
    }

    .metric {
        font-size: 34px;
        font-weight: 800;
        color: #38BDF8;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .subtle {
        color: #CBD5E1;
        font-size: 14px;
    }

    .fixture {
        background: rgba(15, 23, 42, 0.75);
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 12px;
    }

    .fixture-title {
        color: white;
        font-size: 18px;
        font-weight: 700;
    }

    .fixture-small {
        color: #CBD5E1;
        font-size: 14px;
    }

    .good {
        color: #22C55E;
        font-weight: 700;
    }

    .warn {
        color: #FACC15;
        font-weight: 700;
    }

    .error {
        color: #FB7185;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def now_uk():
    return datetime.now(UK_TZ)


def safe_get_json(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def weather_code_to_text(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    return weather_codes.get(code, "Weather unavailable")


def format_fixture_datetime(event):
    timestamp = event.get("strTimestamp")

    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            dt_uk = dt.astimezone(UK_TZ)
            return dt_uk.strftime("%A %d %B %Y, %H:%M")
        except Exception:
            pass

    date_event = event.get("dateEvent") or "Date TBC"
    time_event = event.get("strTime") or "Time TBC"

    return f"{date_event} {time_event}"


# ------------------------------------------------------------
# DATA FUNCTIONS
# ------------------------------------------------------------

@st.cache_data(ttl=1800)
def get_weather():
    params = {
        "latitude": WORTHING_LATITUDE,
        "longitude": WORTHING_LONGITUDE,
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "Europe/London",
        "forecast_days": 3
    }

    data = safe_get_json(OPEN_METEO_URL, params=params)

    if "error" in data:
        return {
            "ok": False,
            "error": data["error"]
        }

    current = data.get("current", {})
    daily = data.get("daily", {})

    return {
        "ok": True,
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "condition": weather_code_to_text(current.get("weather_code")),
        "wind": current.get("wind_speed_10m"),
        "rain_now": current.get("precipitation"),
        "daily_dates": daily.get("time", []),
        "daily_highs": daily.get("temperature_2m_max", []),
        "daily_lows": daily.get("temperature_2m_min", []),
        "daily_rain": daily.get("precipitation_probability_max", []),
        "daily_codes": daily.get("weather_code", [])
    }


@st.cache_data(ttl=3600)
def search_team(team_name):
    url = f"{THESPORTSDB_BASE_URL}/searchteams.php"
    data = safe_get_json(url, params={"t": team_name})

    if "error" in data:
        return None

    teams = data.get("teams") or []

    if not teams:
        return None

    exact_matches = [
        team for team in teams
        if (team.get("strTeam") or "").lower() == team_name.lower()
    ]

    if exact_matches:
        return exact_matches[0]

    partial_matches = [
        team for team in teams
        if team_name.lower() in (team.get("strTeam") or "").lower()
    ]

    if partial_matches:
        return partial_matches[0]

    return teams[0]


@st.cache_data(ttl=3600)
def get_next_fixtures(team_name):
    team = search_team(team_name)

    if not team:
        return {
            "ok": False,
            "team_name": team_name,
            "team_id": None,
            "fixtures": [],
            "error": f"Could not find {team_name} in TheSportsDB."
        }

    team_id = team.get("idTeam")

    url = f"{THESPORTSDB_BASE_URL}/eventsnext.php"
    data = safe_get_json(url, params={"id": team_id})

    if "error" in data:
        return {
            "ok": False,
            "team_name": team.get("strTeam", team_name),
            "team_id": team_id,
            "fixtures": [],
            "error": data["error"]
        }

    fixtures = data.get("events") or []

    return {
        "ok": True,
        "team_name": team.get("strTeam", team_name),
        "team_id": team_id,
        "fixtures": fixtures[:5],
        "badge": team.get("strBadge"),
        "league": team.get("strLeague")
    }


def build_briefing_prompt(weather, men_fixtures, women_fixtures):
    weather_line = "Weather unavailable"

    if weather.get("ok"):
        weather_line = (
            f"Worthing is currently {weather.get('temperature')}°C, "
            f"feels like {weather.get('feels_like')}°C, "
            f"condition: {weather.get('condition')}, "
            f"wind: {weather.get('wind')} km/h."
        )

    def fixture_line(fixtures_result, label):
        fixtures = fixtures_result.get("fixtures", [])
        if not fixtures:
            return f"{label}: fixture data unavailable."

        next_match = fixtures[0]
        home = next_match.get("strHomeTeam", "TBC")
        away = next_match.get("strAwayTeam", "TBC")
        when = format_fixture_datetime(next_match)
        league = next_match.get("strLeague", "Competition TBC")

        return f"{label}: {home} vs {away}, {league}, {when}."

    men_line = fixture_line(men_fixtures, "Manchester United men")
    women_line = fixture_line(women_fixtures, "Manchester United women")

    prompt = f"""
    Write a short, friendly, personal morning briefing for Lisa.

    Make it sound upbeat, useful and natural.
    Keep it concise.
    Do not mention smart metering.
    Do not invent fixture data.
    If something is unavailable, say it naturally.

    Today's date:
    {now_uk().strftime('%A %d %B %Y')}

    Weather:
    {weather_line}

    Football:
    {men_line}
    {women_line}

    Finish with one practical suggestion for the day.
    """

    return prompt


@st.cache_data(ttl=1800)
def generate_gemini_briefing(weather, men_fixtures, women_fixtures):
    if genai is None:
        return {
            "ok": False,
            "text": "Gemini is not installed yet. Add google-genai to requirements.txt, then redeploy."
        }

    gemini_key = st.secrets.get("GEMINI_API_KEY", "")

    if not gemini_key:
        return {
            "ok": False,
            "text": "Gemini is ready to connect. Add your GEMINI_API_KEY in Streamlit Secrets."
        }

    try:
        client = genai.Client(api_key=gemini_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_briefing_prompt(weather, men_fixtures, women_fixtures)
        )

        return {
            "ok": True,
            "text": response.text
        }

    except Exception as e:
        return {
            "ok": False,
            "text": f"Gemini could not generate the briefing: {e}"
        }


# ------------------------------------------------------------
# DISPLAY COMPONENTS
# ------------------------------------------------------------

def fixture_card(title, result):
    fixtures = result.get("fixtures", [])

    st.markdown(f"### {title}")

    if not result.get("ok"):
        st.error(result.get("error", "Fixture data could not be loaded."))
        return

    st.caption(f"{result.get('team_name')} | {result.get('league') or 'League unavailable'}")

    if not fixtures:
        st.warning("No upcoming fixtures returned by the football API.")
        return

    for event in fixtures:
        home = event.get("strHomeTeam", "TBC")
        away = event.get("strAwayTeam", "TBC")
        league = event.get("strLeague", "Competition TBC")
        venue = event.get("strVenue") or "Venue TBC"
        when = format_fixture_datetime(event)

        st.markdown(
            f"""
            <div class="fixture">
                <div class="fixture-title">{home} vs {away}</div>
                <div class="fixture-small">{league}</div>
                <div class="fixture-small">{when}</div>
                <div class="fixture-small">{venue}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def weather_panel(weather):
    if not weather.get("ok"):
        st.error(f"Weather could not be loaded: {weather.get('error')}")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Worthing now", f"{weather.get('temperature')}°C")

    with col2:
        st.metric("Feels like", f"{weather.get('feels_like')}°C")

    with col3:
        st.metric("Wind", f"{weather.get('wind')} km/h")

    with col4:
        st.metric("Rain now", f"{weather.get('rain_now')} mm")

    st.markdown(f"**Condition:** {weather.get('condition')}")

    st.markdown("### 3-day forecast")

    dates = weather.get("daily_dates", [])
    highs = weather.get("daily_highs", [])
    lows = weather.get("daily_lows", [])
    rain = weather.get("daily_rain", [])
    codes = weather.get("daily_codes", [])

    forecast_cols = st.columns(3)

    for i in range(min(3, len(dates))):
        with forecast_colscondition = weather_code_to_text(codes[i]) if i < len(codes) else "Unavailable"
            rain_value = rain[i] if i < len(rain) else "N/A"
            high = highs[i] if i < len(highs) else "N/A"
            low = lows[i] if i < len(lows) else "N/A"

            st.markdown(
                f"""
                <div class="card">
                    <h3>{dates[i]}</h3>
                    <div class="metric">{high}°C</div>
                    <p class="subtle">Low: {low}°C</p>
                    <p class="subtle">{condition}</p>
                    <p class="subtle">Rain chance: {rain_value}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

weather = get_weather()
men_fixtures = get_next_fixtures(MEN_TEAM_NAME)
women_fixtures = get_next_fixtures(WOMEN_TEAM_NAME)


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title("🚀 Lisa's Daily Pulse")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Football",
        "Weather",
        "AI Briefing",
        "Learning",
        "Goals"
    ]
)

st.sidebar.markdown("---")

if weather.get("ok"):
    st.sidebar.success(f"Worthing: {weather.get('temperature')}°C")
else:
    st.sidebar.warning("Weather unavailable")

if men_fixtures.get("ok"):
    st.sidebar.success("Men's fixtures loaded")
else:
    st.sidebar.warning("Men's fixtures issue")

if women_fixtures.get("ok"):
    st.sidebar.success("Women's fixtures loaded")
else:
    st.sidebar.warning("Women's fixtures issue")


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

if page == "Home":

    st.markdown(
        f"""
        <div class="hero">
            <h1>☕ Good Morning Lisa</h1>
            <p>{now_uk().strftime('%A %d %B %Y, %H:%M')}</p>
            <p>Your personal daily briefing, football hub and morning command centre.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        temp_display = f"{weather.get('temperature')}°C" if weather.get("ok") else "Unavailable"
        condition_display = weather.get("condition") if weather.get("ok") else "Weather not loaded"

        st.markdown(
            f"""
            <div class="card">
                <h3>🌦 Worthing Weather</h3>
                <div class="metric">{temp_display}</div>
                <p>{condition_display}</p>
                <p class="subtle">Powered by Open-Meteo</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        men_next = men_fixtures.get("fixtures", [])

        if men_next:
            event = men_next[0]
            title = f"{event.get('strHomeTeam', 'TBC')} vs {event.get('strAwayTeam', 'TBC')}"
            when = format_fixture_datetime(event)
        else:
            title = "Fixture unavailable"
            when = men_fixtures.get("error", "No fixture returned")

        st.markdown(
            f"""
            <div class="card">
                <h3>⚽ United Men</h3>
                <div class="metric">Next Match</div>
                <p>{title}</p>
                <p class="subtle">{when}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        women_next = women_fixtures.get("fixtures", [])

        if women_next:
            event = women_next[0]
            title = f"{event.get('strHomeTeam', 'TBC')} vs {event.get('strAwayTeam', 'TBC')}"
            when = format_fixture_datetime(event)
        else:
            title = "Fixture unavailable"
            when = women_fixtures.get("error", "No fixture returned")

        st.markdown(
            f"""
            <div class="card">
                <h3>⚽ United Women</h3>
                <div class="metric">Next Match</div>
                <p>{title}</p>
                <p class="subtle">{when}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🤖 Lisa's AI Morning Briefing")

    briefing = generate_gemini_briefing(weather, men_fixtures, women_fixtures)

    if briefing.get("ok"):
        st.success(briefing.get("text"))
    else:
        st.info(briefing.get("text"))

    st.markdown("---")

    st.markdown("## Quick view")

    col_a, col_b = st.columns(2)

    with col_a:
        fixture_card("Manchester United Men", men_fixtures)

    with col_b:
        fixture_card("Manchester United Women", women_fixtures)


# ------------------------------------------------------------
# FOOTBALL
# ------------------------------------------------------------

elif page == "Football":

    st.title("⚽ Football Hub")

    col1, col2 = st.columns(2)

    with col1:
        fixture_card("Manchester United Men", men_fixtures)

    with col2:
        fixture_card("Manchester United Women", women_fixtures)

    st.caption("Fixture data comes from TheSportsDB. If a team does not return fixtures, the API may not currently have upcoming events for that team.")


# ------------------------------------------------------------
# WEATHER
# ------------------------------------------------------------

elif page == "Weather":

    st.title("🌦 Worthing Weather")
    weather_panel(weather)


# ------------------------------------------------------------
# AI BRIEFING
# ------------------------------------------------------------

elif page == "AI Briefing":

    st.title("🤖 Lisa AI Briefing")

    briefing = generate_gemini_briefing(weather, men_fixtures, women_fixtures)

    if briefing.get("ok"):
        st.success(briefing.get("text"))
    else:
        st.warning(briefing.get("text"))

    st.markdown("---")

    st.markdown("### Source data being sent to Gemini")

    st.json(
        {
            "weather": weather,
            "men_fixtures": men_fixtures,
            "women_fixtures": women_fixtures
        }
    )


# ------------------------------------------------------------
# LEARNING
# ------------------------------------------------------------

elif page == "Learning":

    st.title("📚 Learning Centre")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            ### Data skills

            - Python
            - Streamlit
            - Power BI
            - SQL
            - APIs
            """
        )

    with col2:
        st.markdown(
            """
            ### AI skills

            - Gemini API
            - Prompt engineering
            - Personal automation
            - App building
            - GitHub deployment
            """
        )

    st.success("You are already building a proper deployed app. This is exactly how you learn it.")


# ------------------------------------------------------------
# GOALS
# ------------------------------------------------------------

elif page == "Goals":

    st.title("🎯 Personal Goals")

    st.checkbox("Deploy first Streamlit app", value=True)
    st.checkbox("Connect free weather API", value=True)
    st.checkbox("Connect Man United fixtures", value=True)
    st.checkbox("Connect Gemini AI")
    st.checkbox("Make it look premium")
    st.checkbox("Add personalised news")

    st.progress(70)

    st.success("Current status: website is live, weather is live, football is connected, Gemini is ready once the secret key is added.")
