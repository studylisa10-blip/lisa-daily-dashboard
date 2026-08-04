%%writefile main.py
import streamlit as st
from datetime import datetime

# --- Custom CSS for Premium Look (Dark Theme, Fonts, Cards, etc.) ---
CSS_CODE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        color: #e0e0e0; /* Light gray for text */
        background-color: #0d1117; /* Dark background */
    }

    .stApp {
        background-color: #0d1117;
        color: #e0e0e0;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    .st-emotion-cache-vk33as.e1fqkh3o10 {
        background-color: #161b22; /* Slightly lighter dark for sidebar */
        color: #e0e0e0;
        border-right: 1px solid #21262d;
        padding-top: 2rem;
    }
    
    /* Sidebar title */
    .st-emotion-cache-vk33as.e1fqkh3o10 h1 {
        color: #58a6ff; /* A nice blue for titles */
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
        text-shadow: 0 0 5px rgba(88, 166, 255, 0.5);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff; /* A nice blue for titles */
        font-weight: 600;
    }
    h1 {
        font-size: 2.5em;
        margin-bottom: 0.5em;
        text-align: center;
    }
    h2 {
        font-size: 2em;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
        border-bottom: 1px solid #21262d;
        padding-bottom: 0.5em;
    }

    /* Cards */
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        justify-content: center;
        margin-top: 1.5rem;
    }

    .st-emotion-cache-nahz7x.e1fqkh3o3, .st-emotion-cache-zt5ig5.e1fqkh3o3, .st-emotion-cache-5rimss.e1fqkh3o3, .st-emotion-cache-gh2jqy.e1fqkh3o3, .st-emotion-cache-fybf3f.e1fqkh3o3, .st-emotion-cache-zt5ig5.e1fqkh3o3, .st-emotion-cache-fybf3f.e1fqkh3o3 {
        background-color: #161b22; /* Card background */
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); /* Subtle shadow */
        transition: all 0.3s ease-in-out;
        border: 1px solid #21262d;
    }
    .st-emotion-cache-nahz7x.e1fqkh3o3:hover, .st-emotion-cache-zt5ig5.e1fqkh3o3:hover, .st-emotion-cache-5rimss.e1fqkh3o3:hover, .st-emotion-cache-gh2jqy.e1fqkh3o3:hover, .st-emotion-cache-fybf3f.e1fqkh3o3:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }

    /* Buttons */
    .stButton>button {
        background-color: #238636; /* GitHub green */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }

    /* Text input */
    .st-emotion-cache-ue6h4q, .st-emotion-cache-16qf7f7 {
        background-color: #21262d;
        border-radius: 5px;
        border: 1px solid #30363d;
        color: #e0e0e0;
    }

    /* Metric boxes */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        border: 1px solid #21262d;
    }
    [data-testid="stMetric"] > div > div:first-child {
        color: #58a6ff;
    }
    [data-testid="stMetricValue"] {
        color: #e0e0e0;
        font-size: 1.8em;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #161b22;
        border-radius: 8px;
        border: 1px solid #21262d;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        color: #e0e0e0;
    }
    .streamlit-expanderContent {
        background-color: #0d1117;
        border-left: 3px solid #58a6ff;
        padding-left: 1rem;
        margin-left: 0.5rem;
    }
    
    /* Links */
    a {
        color: #58a6ff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    
    /* Gradient effect for certain elements (can be applied manually) */
    .gradient-text {
        background: linear-gradient(90deg, #58a6ff, #8a58ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2em;
        }
        .main .block-container {
            padding: 1rem;
        }
    }

</style>
"""

st.set_page_config(
    page_title="Lisa's Daily Briefing",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CSS_CODE, unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h1><span class='gradient-text'>Lisa's Briefing</span></h1>", unsafe_allow_html=True)
    st.image("https://i.ibb.co/VvzK29t/lisa-avatar.png", use_column_width=True) # Placeholder for an avatar or logo
    st.markdown("--- ")
    
    st.subheader("Navigation")
    selected_page = st.radio(
        "Go to",
        ["Home", "Man Utd Men's", "Man Utd Women's", "Football News", "UK News", "World News", "Tech News", "AI News", "Weather", "Learning & Self-Development", "Interesting Facts", "Recommendations"],
        index=0
    )
    st.markdown("--- ")
    st.write("© 2023 Lisa's Daily Briefing")

# --- Main Content Area ---
if selected_page == "Home":
    st.markdown("<h1><span class='gradient-text'>Good Morning Lisa!</span></h1>", unsafe_allow_html=True)
    
    current_dt = datetime.now()
    st.write(f"### Today is: {current_dt.strftime('%A, %B %d, %Y')}")
    st.write(f"### Current Time: {current_dt.strftime('%H:%M:%S')}")
    
    st.markdown("--- ")
    
    st.subheader("🤖 AI-Generated Daily Summary")
    st.info("Placeholder for a concise AI-generated summary of your day's important information.")
    
    st.markdown("## Your Dashboard Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="New Emails", value="5", delta="2 new")
    with col2:
        st.metric(label="Calendar Events", value="3", delta="1 upcoming")
    with col3:
        st.metric(label="Weather Alert", value="Clear", delta="68°F")

    st.markdown("--- ")
    st.subheader("Quick Links & Highlights")
    st.write("Here you'll find quick links to key information.")
    
    st.columns(1)[0].markdown("### Placeholder Card Example", unsafe_allow_html=True)
    st.columns(1)[0].markdown(
        """
        <div class="card-container">
            <div class="st-emotion-cache-nahz7x e1fqkh3o3" style="flex: 1 1 calc(33% - 1.5rem); min-width: 280px;">
                <h4>Manchester United</h4>
                <p>Next Match: Man Utd vs. City (Tomorrow)</p>
                <img src="https://i.ibb.co/L5h8z9c/manutd.png" alt="Man Utd" style="width:100%; border-radius: 8px;">
            </div>
            <div class="st-emotion-cache-nahz7x e1fqkh3o3" style="flex: 1 1 calc(33% - 1.5rem); min-width: 280px;">
                <h4>Top Story</h4>
                <p>Global AI Summit Concludes with Major Breakthroughs</p>
                <img src="https://i.ibb.co/fQ2h25D/ai-news.png" alt="AI News" style="width:100%; border-radius: 8px;">
            </div>
            <div class="st-emotion-cache-nahz7x e1fqkh3o3" style="flex: 1 1 calc(33% - 1.5rem); min-width: 280px;">
                <h4>Weather Today</h4>
                <p>Sunny with a chance of afternoon showers. High 72°F.</p>
                <img src="https://i.ibb.co/BfK0X0F/weather.png" alt="Weather" style="width:100%; border-radius: 8px;">
            </div>
        </div>
        """, unsafe_allow_html=True
    )


elif selected_page == "Man Utd Men's":
    st.header("⚽ Manchester United Men's Fixtures")
    st.write("Upcoming matches and results for the Men's team.")
    st.info("Content for Men's fixtures will go here.")

elif selected_page == "Man Utd Women's":
    st.header("⚽ Manchester United Women's Fixtures")
    st.write("Upcoming matches and results for the Women's team.")
    st.info("Content for Women's fixtures will go here.")

elif selected_page == "Football News":
    st.header("📰 Latest Football News")
    st.write("Breaking news and updates from the world of football.")
    st.info("Content for Football News will go here.")

elif selected_page == "UK News":
    st.header("🇬🇧 UK News")
    st.write("Top headlines from around the United Kingdom.")
    st.info("Content for UK News will go here.")

elif selected_page == "World News":
    st.header("🌎 World News")
    st.write("Global news and current events.")
    st.info("Content for World News will go here.")

elif selected_page == "Tech News":
    st.header("💻 Technology News")
    st.write("The latest in tech innovations and industry news.")
    st.info("Content for Technology News will go here.")

elif selected_page == "AI News":
    st.header("🤖 AI News")
    st.write("Developments and breakthroughs in Artificial Intelligence.")
    st.info("Content for AI News will go here.")

elif selected_page == "Weather":
    st.header("🌤️ Current Weather & Forecast")
    st.write("Your local weather update and forecast.")
    st.info("Content for Weather will go here.")

elif selected_page == "Learning & Self-Development":
    st.header("📚 Learning & Self-Development")
    st.write("Resources and insights for personal growth.")
    st.info("Content for Learning & Self-Development will go here.")

elif selected_page == "Interesting Facts":
    st.header("💡 Interesting Facts")
    st.write("A daily dose of fascinating information.")
    st.info("Content for Interesting Facts will go here.")

elif selected_page == "Recommendations":
    st.header("🌟 Today's Recommendations")
    st.write("Personalized recommendations for articles, books, or activities.")
    st.info("Content for Today's Recommendations will go here.")

