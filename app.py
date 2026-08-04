import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Lisa's Daily Pulse",
    page_icon="🚀",
    layout="wide"
)

# ---------- CUSTOM CSS ----------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
}

.hero {
    background: linear-gradient(135deg, #18A0FB, #7B61FF);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    height: 220px;
}

h1, h2, h3 {
    color: white;
}

.metric {
    font-size: 28px;
    font-weight: bold;
    color: #38BDF8;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------

st.sidebar.title("🚀 Lisa's Daily Pulse")

st.sidebar.markdown("---")

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

    st.markdown(f"""
    <div class="hero">
        <h1>☕ Good Morning Lisa</h1>
        <p>{datetime.now().strftime("%A %d %B %Y")}</p>
        <p>Your personal daily briefing and command centre.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>⚽ Next Men's Match</h3>
            <p>Manchester United</p>
            <div class="metric">TBC</div>
            <p>Live fixtures coming soon</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚽ Next Women's Match</h3>
            <p>Manchester United Women</p>
            <div class="metric">TBC</div>
            <p>Live fixtures coming soon</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🌦 Weather</h3>
            <p>Worthing</p>
            <div class="metric">--°C</div>
            <p>Live forecast coming soon</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🤖 Daily AI Briefing")

    st.info("""
    Welcome back Lisa.

    This dashboard will eventually give you:
    • Football fixtures
    • Personalised news
    • Weather
    • AI summaries
    • Learning recommendations

    Your very own daily newspaper.
    """)

# ---------- FOOTBALL ----------

elif page == "Football":

    st.title("⚽ Football Hub")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Manchester United Men")
        st.write("Fixtures, results and league table coming soon.")

    with col2:
        st.subheader("Manchester United Women")
        st.write("Fixtures, results and league table coming soon.")

# ---------- NEWS ----------

elif page == "News":

    st.title("📰 News Centre")

    st.subheader("Top Stories")

    st.write("• UK News")
    st.write("• World News")
    st.write("• Technology News")
    st.write("• AI News")

# ---------- LEARNING ----------

elif page == "Learning":

    st.title("📚 Learning Centre")

    st.write("Power BI")
    st.write("Databricks")
    st.write("Python")
    st.write("Artificial Intelligence")

# ---------- GOALS ----------

elif page == "Goals":

    st.title("🎯 Personal Goals")

    st.write("Books")
    st.write("Travel plans")
    st.write("Projects")
    st.write("Learning targets")
