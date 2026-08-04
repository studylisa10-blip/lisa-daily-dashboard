import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from google import genai
except Exception:
    genai = None


# ------------------------------------------------------------
# PAGE SETUP
# ------------------------------------------------------------

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

UK_TZ = ZoneInfo("Europe/London")

WORTHING_LAT = 50.817
WORTHING_LON = -0.375

SPORTSDB_KEY = "123"
SPORTSDB_BASE = f"https://www.thesportsdb.com/api/v1/json/{SPORTSDB_KEY}"


# ------------------------------------------------------------
# STYLE
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
        margin-bottom: 25px;
        box-shadow: 0px 12px 30px rgba(0,0,0,0.30);
    }

    .hero h1 {
        color: white;
        font-size: 44px;
        margin-bottom: 5px;
    }

    .hero p {
        color: white;
        font-size: 16px;
    }

    .card {
        background: rgba(30, 41, 59, 0.95);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #334155;
        min-height: 220px;
        box-shadow: 0px 10px 24px rgba(0,0,0,0.22);
        margin-bottom: 18px;
    }

    .card h3 {
        color: white;
    }

    .metric {
        font-size: 32px;
        font-weight: 800;
        color: #38BDF8;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .small {
        color: #CBD5E1;
        font-size: 14px;
    }

    .fixture {
        background: rgba(15, 23, 42, 0.75);
        padding: 16px;
        border-radius: 15px;
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
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def now_uk():
    return datetime.now(UK_TZ)


def safe_json(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def weather_code_to_text(code):
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Freezing fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Light rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Heavy thunderstorm with hail"
    }

    return codes.get(code, "Weather unavailable")


def format_match_time(event):
    timestamp = event.get("strTimestamp")

    if timestamp:
        try:
            match_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            match_dt = match_dt.astimezone(UK_TZ)
            return match_dt.strftime("%A %d %B %Y, %H:%M")
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
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": WORTHING_LAT,
        "longitude": WORTHING_LON,
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "Europe/London",
        "forecast_days": 3
    }

    data = safe_json(url, params)

    if "error" in data:
        return {
            "ok": False,
            "error": data["error"]
        }

    current = data.get("current", {})
    daily = data.get("daily", {})

    return {
        "ok": True,
        "temp": current.get("temperature_2m"),
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
def find_team(team_name):
    url = f"{SPORTSDB_BASE}/searchteams.php"

    data = safe_json(url, {"t": team_name})

    if "error" in data:
        return None

    teams = data.get("teams") or []

    if not teams:
        return None

    for team in teams:
        if (team.get("strTeam") or "").lower() == team_name.lower():
            return team

    return teams[0]


@st.cache_data(ttl=3600)
def get_next_fixtures(team_name):
    team = find_team(team_name)

    if not team:
        return {
            "ok": False,
            "team": team_name,
            "fixtures": [],
            "error": f"Could not find {team_name}."
        }

    team_id = team.get("idTeam")
    url = f"{SPORTSDB_BASE}/eventsnext.php"

    data = safe_json(url, {"id": team_id})

    if "error" in data:
        return {
            "ok": False,
            "team": team.get("strTeam", team_name),
            "fixtures": [],
            "error": data["error"]
        }

    fixtures = data.get("events") or []

    return {
        "ok": True,
        "team": team.get("strTeam", team_name),
        "league": team.get("strLeague"),
        "badge": team.get("strBadge"),
        "fixtures": fixtures[:5]
    }


def build_ai_prompt(weather, men, women):
    if weather.get("ok"):
        weather_text = (
            f"Worthing is {weather.get('temp')} degrees Celsius, "
            f"feels like {weather.get('feels_like')} degrees, "
            f"condition is {weather.get('condition')}, "
            f"wind is {weather.get('wind')} km/h."
        )
    else:
        weather_text = "Weather is unavailable."

    def fixture_text(data, label):
        fixtures = data.get("fixtures", [])

        if not fixtures:
            return f"{label}: fixture data unavailable."

        event = fixtures[0]
        home = event.get("strHomeTeam", "TBC")
        away = event.get("strAwayTeam", "TBC")
        comp = event.get("strLeague", "Competition TBC")
        when = format_match_time(event)

        return f"{label}: {home} vs {away}, {comp}, {when}."

    men_text = fixture_text(men, "Manchester United men")
    women_text = fixture_text(women, "Manchester United women")

    return f"""
    Write a short personal morning briefing for Lisa.

    Tone:
    Friendly, upbeat and useful.

    Rules:
    Do not mention smart metering.
    Do not invent data.
    If something is unavailable, say it naturally.
    Keep it short.

    Date:
    {now_uk().strftime("%A %d %B %Y")}

    Weather:
    {weather_text}

    Football:
    {men_text}
    {women_text}

    End with one practical suggestion for the day.
    """


@st.cache_data(ttl=1800)
def get_gemini_briefing(weather, men, women):
    if genai is None:
        return {
            "ok": False,
            "text": "Gemini is not installed yet. Add google-genai to requirements.txt."
        }

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        return {
            "ok": False,
            "text": "Gemini is ready, but you need to add your GEMINI_API_KEY in Streamlit Secrets."
        }

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_ai_prompt(weather, men, women)
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
# DISPLAY FUNCTIONS
# ------------------------------------------------------------

def show_fixture_list(title, data):
    st.markdown(f"### {title}")

    if not data.get("ok"):
        st.warning(data.get("error", "Fixtures unavailable."))
        return

    st.caption(f"{data.get('team')} | {data.get('league') or 'League unavailable'}")

    fixtures = data.get("fixtures", [])

    if not fixtures:
        st.warning("No upcoming fixtures found.")
        return

    for event in fixtures:
        home = event.get("strHomeTeam", "TBC")
        away = event.get("strAwayTeam", "TBC")
        league = event.get("strLeague", "Competition TBC")
        venue = event.get("strVenue") or "Venue TBC"
        when = format_match_time(event)

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


def show_weather(weather):
    if not weather.get("ok"):
        st.error(weather.get("error", "Weather unavailable."))
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Worthing now", f"{weather.get('temp')}°C")

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

    cols = st.columns(3)

    for i in range(min(3, len(dates))):
        high = highs[i] if i < len(highs) else "N/A"
        low = lows[i] if i < len(lows) else "N/A"
        rain_chance = rain[i] if i < len(rain) else "N/A"
        condition = weather_code_to_text(codes[i]) if i < len(codes) else "Unavailable"

        with colsst.markdown(
                f"""
                <div class="card">
                    <h3>{dates[i]}</h3>
                    <div class="metric">{high}°C</div>
                    <p class="small">Low: {low}°C</p>
                    <p class="small">{condition}</p>
                    <p class="small">Rain chance: {rain_chance}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )


def next_fixture_text(data):
    fixtures = data.get("fixtures", [])

    if not fixtures:
        return "Fixture unavailable", data.get("error", "No fixture returned")

    event = fixtures[0]
    title = f"{event.get('strHomeTeam', 'TBC')} vs {event.get('strAwayTeam', 'TBC')}"
    when = format_match_time(event)

    return title, when


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

weather = get_weather()
men_fixtures = get_next_fixtures("Manchester United")
women_fixtures = get_next_fixtures("Manchester United Women")


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
    st.sidebar.success(f"Weather: {weather.get('temp')}°C")
else:
    st.sidebar.warning("Weather issue")

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
            <p>{now_uk().strftime("%A %d %B %Y, %H:%M")}</p>
            <p>Your personal daily briefing, football hub and morning command centre.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if weather.get("ok"):
            temp = f"{weather.get('temp')}°C"
            condition = weather.get("condition")
        else:
            temp = "Unavailable"
            condition = "Weather not loaded"

        st.markdown(
            f"""
            <div class="card">
                <h3>🌦 Worthing Weather</h3>
                <div class="metric">{temp}</div>
                <p>{condition}</p>
                <p class="small">Powered by Open-Meteo</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        men_title, men_when = next_fixture_text(men_fixtures)

        st.markdown(
            f"""
            <div class="card">
                <h3>⚽ United Men</h3>
                <div class="metric">Next Match</div>
                <p>{men_title}</p>
                <p class="small">{men_when}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        women_title, women_when = next_fixture_text(women_fixtures)

        st.markdown(
            f"""
            <div class="card">
                <h3>⚽ United Women</h3>
                <div class="metric">Next Match</div>
                <p>{women_title}</p>
                <p class="small">{women_when}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🤖 Lisa's AI Morning Briefing")

    briefing = get_gemini_briefing(weather, men_fixtures, women_fixtures)

    if briefing.get("ok"):
        st.success(briefing.get("text"))
    else:
        st.info(briefing.get("text"))

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        show_fixture_list("Manchester United Men", men_fixtures)

    with col_b:
        show_fixture_list("Manchester United Women", women_fixtures)


# ------------------------------------------------------------
# FOOTBALL
# ------------------------------------------------------------

elif page == "Football":

    st.title("⚽ Football Hub")

    col1, col2 = st.columns(2)

    with col1:
        show_fixture_list("Manchester United Men", men_fixtures)

    with col2:
        show_fixture_list("Manchester United Women", women_fixtures)

    st.caption("Football data is loaded from TheSportsDB. If a fixture is missing, the API may not currently have that team schedule available.")


# ------------------------------------------------------------
# WEATHER
# ------------------------------------------------------------

elif page == "Weather":

    st.title("🌦 Worthing Weather")
    show_weather(weather)


# ------------------------------------------------------------
# AI BRIEFING
# ------------------------------------------------------------

elif page == "AI Briefing":

    st.title("🤖 Lisa AI Briefing")

    briefing = get_gemini_briefing(weather, men_fixtures, women_fixtures)

    if briefing.get("ok"):
        st.success(briefing.get("text"))
    else:
        st.warning(briefing.get("text"))

    with st.expander("View source data"):
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
            - APIs
            - GitHub
            - Data visualisation
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
            - AI summaries
            """
        )

    st.success("You are building a real deployed app. This is exactly how you learn it.")


# ------------------------------------------------------------
# GOALS
# ------------------------------------------------------------

elif page == "Goals":

    st.title("🎯 Personal Goals")

    st.checkbox("Deploy first Streamlit app", value=True)
    st.checkbox("Add Open-Meteo weather", value=True)
    st.checkbox("Add Man United fixtures", value=True)
    st.checkbox("Add Gemini AI briefing")
    st.checkbox("Add personalised news")
    st.checkbox("Make it look premium", value=True)

    st.progress(70)

    st.success("Current status: website is live, weather is connected, football is connected, Gemini is ready once the secret key is added.")
