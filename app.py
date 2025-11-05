import streamlit as st
import google.generativeai as genai
from utils.rag_utils import retrieve_relevant_context, process_pdf_upload
from utils.firebase_utils import save_user_data, init_firebase, log_chat_to_firebase, get_analytics_data
import datetime
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Medical Research Assistant 👨🏻‍⚕️", page_icon="🩺", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f9fafb;
            padding: 2rem;
            border-radius: 15px;
        }
        .stTextInput, .stNumberInput {
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 8px 20px;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ FIREBASE INITIALIZATION------------------
init_firebase("firebase_config.json")

# ------------------ GEMINI CONFIGURATION ------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# ------------------ OFFLINE FALLBACK IN CASE IF MODEL FAILS TO LOAD ------------------
offline_fallback = {
    "what is diabetes": "Diabetes is a chronic condition that affects how your body turns food into energy.",
    "what is heart disease": "Heart disease refers to a range of conditions that affect your heart’s function or structure.",
    "what is hypertension": "Hypertension is another term for high blood pressure — a condition where the pressure in arteries is persistently high.",
    "what is anemia": "Anemia occurs when your blood doesn’t have enough healthy red blood cells to carry oxygen to your body’s tissues."
}

# ------------------ EMERGENCY NUMBERS ------------------
emergency_numbers = {
    "🚑 Ambulance": "108",
    "🏥 Medical Helpline": "104",
    "👮 Police": "100",
    "🔥 Fire": "101",
    "🧠  Hospital Helpline": "915xxxxxx (Apollo Helpline, India)"
}

# ------------------ HELPER FUNCTIONS ------------------
def check_gemini_status():
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content("ping")
        if response and response.text:
            return True
    except Exception as e:
        print("Gemini status check error:", e)
    return False


def get_gemini_response(user_query, context):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        prompt = f"""
        You are a professional medical research assistant. Use the following context:
        {context}

        User question: {user_query}
        Provide clear, factual, and empathetic medical guidance.
        """
        response = model.generate_content(prompt)
        return response.text if response and response.text else "⚠️ No response from Gemini."
    except Exception as e:
        print("Error from Gemini:", e)
        return None

# ------------------ SIDEBAR ------------------
st.sidebar.header("🚨 Emergency Contacts")
for service, number in emergency_numbers.items():
    st.sidebar.write(f"**{service}:** {number}")

st.sidebar.divider()
st.sidebar.header("📄 Knowledge Base Upload")
uploaded_pdf = st.sidebar.file_uploader("Upload Medical Research PDF", type=["pdf"])
if uploaded_pdf:
    with st.spinner("Processing PDF..."):
        process_pdf_upload(uploaded_pdf)
    st.sidebar.success("✅ PDF added to knowledge base.")

# ------------------ TO SEE CONNECTION STATUS OF MODEL ------------------
is_online = check_gemini_status()
if is_online:
    st.sidebar.success("✅ Gemini 2.5 Pro Online")
else:
    st.sidebar.error("🔴 Gemini Offline (Using fallback)")

# ------------------ MAIN TABS ------------------
tab1, tab2 = st.tabs(["💬 Chat Assistant", "📊 Analytics Dashboard"])

# ------------------ CHAT TAB ------------------
with tab1:
    st.title("🩺 Medical Research Assistant 👨🏻‍⚕️👨🏻‍⚕️")
    st.caption("Your trusted AI for medical research and emergency guidance.")

    if "user" not in st.session_state:
        with st.form("user_form"):
            name = st.text_input("👤 Name:")
            age = st.number_input("🎂 Age:", min_value=1, max_value=120)
            submitted = st.form_submit_button("Start Chat")
            if submitted and name:
                st.session_state.user = {"name": name, "age": age}
                st.session_state.chat_history = []
                save_user_data(name, age)
                st.success(f"Welcome {name}! You can now start chatting.")
    else:
        st.info(f"👋 Hi {st.session_state.user['name']}, ask me any medical question.")
        user_query = st.text_input("💬 Enter your question:")

        if user_query:
            st.session_state.chat_history.append({
                "role": "user",
                "text": user_query,
                "time": datetime.datetime.now().strftime("%H:%M")
            })

            context = retrieve_relevant_context(user_query)
            bot_reply = get_gemini_response(user_query, context) if is_online else None

            if not bot_reply:
                bot_reply = next((v + " (Offline mode)" for k, v in offline_fallback.items() if k in user_query.lower()), 
                                 "⚠️ Offline and no response available.")

            st.session_state.chat_history.append({
                "role": "bot",
                "text": bot_reply,
                "time": datetime.datetime.now().strftime("%H:%M")
            })

            log_chat_to_firebase(st.session_state.user["name"], user_query, bot_reply)

        # Display chat messages
        for msg in reversed(st.session_state.get("chat_history", [])):
            if msg["role"] == "user":
                st.markdown(f"🧑‍⚕️ **You ({msg['time']}):** {msg['text']}")
            else:
                st.markdown(f"🤖 **Assistant ({msg['time']}):** {msg['text']}")

# ------------------ ANALYTICS TAB ------------------
with tab2:
    st.title("📊 Analytics Dashboard")
    st.caption("Monitor app usage, trends, and most common queries.")

    data = get_analytics_data()
    if data.empty:
        st.warning("No analytics data available yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(data, x="query", y="count", title="Top Medical Queries", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig2 = px.pie(data, names="query", values="count", title="Query Distribution")
            st.plotly_chart(fig2, use_container_width=True)
##--------------------END----------------------------------------------------------