import streamlit as st
import requests

try:
    from google import genai
except:
    genai = None

st.set_page_config(
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
# FOOTBALL
# --------------------------

def get_mens_fixture():

    url = "https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id=133612"

    data = requests.get(url).json()

    fixtures = data.get("events", [])

    if fixtures:
        return fixtures[0]

    return None

# --------------------------
# GEMINI
# --------------------------

def get_briefing(temp, fixture):

    if genai is None:
        return "Gemini package not installed."

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return "Add your GEMINI_API_KEY in Streamlit Secrets."

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""

        You are Lisa's personal morning assistant.

        Current weather:
        {temp}°C in Worthing

        Next Manchester United fixture:
        {fixture}

        Write a short friendly morning briefing.
        Mention the weather.
        Mention the football.
        End with one motivational sentence.

        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini error: {e}"

# --------------------------
# PAGE
# --------------------------

st.title("🚀 Lisa's Daily Pulse")

col1, col2 = st.columns(2)

temp = get_weather()

fixture = get_mens_fixture()

with col1:

    st.metric(
        label="🌦 Worthing Temperature",
        value=f"{temp} °C"
    )

with col2:

    st.subheader("⚽ Manchester United Men")

    if fixture:

        fixture_text = (
            f"{fixture['strHomeTeam']} vs "
            f"{fixture['strAwayTeam']} "
            f"({fixture['dateEvent']})"
        )

        st.write(fixture_text)

    else:

        fixture_text = "Fixture unavailable"

        st.write(fixture_text)

st.divider()

st.subheader("🤖 Morning AI Briefing")

briefing = get_briefing(
    temp,
    fixture_text
)

st.write(briefing)
