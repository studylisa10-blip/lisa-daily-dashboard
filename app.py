import streamlit as st
from datetime import datetime
import random

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# ---------- STYLING ----------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
}

.hero {
    background: linear-gradient(135deg,#18A0FB,#7B61FF);
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.metric {
    font-size: 32px;
    font-weight: bold;
    color: #38BDF8;
}

.small {
    color: #94A3B8;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------

st.sidebar.title("🚀 Lisa's Daily Pulse")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Football",
        "News",
        "Learning",
        "Goals"
    ]
)

# ---------- HOME ----------

if page == "Home":

    quotes = [
        "Small improvements every day lead to massive results.",
        "Today's progress is tomorrow's success.",
        "Done is better than perfect.",
        "Focus on progress, not perfection.",
        "The best project you'll ever build is yourself."
    ]

    st.markdown(f"""
    <div class='hero'>
        <h1>☕ Good Morning Lisa</h1>
        <h4>{datetime.now().strftime('%A %d %B %Y')}</h4>
        <p>Welcome to your personal daily briefing.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
        <h3>⚽ Football</h3>
        <div class='metric'>MUFC</div>
        <p>Check latest fixtures and news.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
        <h3>🌦 Weather</h3>
        <div class='metric'>Worthing</div>
        <p>Ready for live weather feeds.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card'>
        <h3>📰 News</h3>
        <div class='metric'>Daily</div>
        <p>Personalised briefings.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🤖 Daily Briefing")

    st.info(
        f"""
        Good morning Lisa.

        Your dashboard is now live ✅

        Next steps:
        • Add live football fixtures
        • Add live weather
        • Add real news feeds
        • Connect Gemini AI

        💡 Quote of the Day:

        "{random.choice(quotes)}"
        """
    )

# ---------- FOOTBALL ----------

elif page == "Football":

    st.title("⚽ Football Hub")

    st.metric(
        label="Favourite Club",
        value="Manchester United"
    )

    st.markdown("---")

    st.subheader("Men's Team")

    st.write("""
    • Latest fixtures
    • Results
    • League table
    • Transfer news
    """)

    st.markdown("---")

    st.subheader("Women's Team")

    st.write("""
    • Latest fixtures
    • Results
    • League table
    • Women's football news
    """)

# ---------- NEWS ----------

elif page == "News":

    st.title("📰 News Centre")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        ### 🇬🇧 UK News

        • Headline 1

        • Headline 2

        • Headline 3
        """)

    with col2:

        st.markdown("""
        ### 🌍 World News

        • Headline 1

        • Headline 2

        • Headline 3
        """)

    st.markdown("---")

    st.markdown("""
    ### 🤖 AI & Technology

    • OpenAI

    • Google Gemini

    • Microsoft AI

    • Databricks
    """)

# ---------- LEARNING ----------

elif page == "Learning":

    st.title("📚 Learning Centre")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Data

        • SQL

        • Power BI

        • Databricks

        • Python
        """)

    with col2:
        st.markdown("""
        ### AI

        • Gemini

        • ChatGPT

        • Prompt Engineering

        • Automation
        """)

# ---------- GOALS ----------

elif page == "Goals":

    st.title("🎯 Personal Goals")

    st.checkbox("Learn Streamlit")
    st.checkbox("Build AI Dashboard")
    st.checkbox("Learn Gemini API")
    st.checkbox("Deploy Personal Website")

    st.progress(25)

    st.success(
        "You've already completed the hardest step: deploying your first app 🚀"
    )
