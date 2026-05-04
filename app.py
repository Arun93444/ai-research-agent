import streamlit as st
import os
import requests
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

gemini_key = os.environ.get("GEMINI_API_KEY")
serpapi_key = os.environ.get("SERPAPI_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
* { font-family: 'DM Sans', sans-serif !important; }
.stApp { background-color: #0d0d0f; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stTextInput input {
    background: #141416 !important;
    border: 1px solid #2a2a2e !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
}
.stButton button {
    background: linear-gradient(135deg, #7c6af7, #4fc3f7) !important;
    border: none !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px !important;
}
.result-box {
    background: #141416;
    border: 1px solid #2a2a2e;
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
    color: #f0f0f0;
}
.step-box {
    background: rgba(124,106,247,0.1);
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 13px;
    color: #a89ef5;
}
hr { border-color: #2a2a2e !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align:center;padding:20px 0 10px">
    <div style="font-size:2.5rem;font-weight:800;
    background:linear-gradient(135deg,#7c6af7,#4fc3f7);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
        🤖 AI Research Agent
    </div>
    <div style="color:#888;font-size:0.9rem;margin-top:4px">
        Give me any topic — I will research it automatically!
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Quick topics
st.markdown("**Quick Topics:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("Latest AI trends 2025"):
        st.session_state.topic = "Latest AI trends 2025"
with col2:
    if st.button("How to get AI job in India"):
        st.session_state.topic = "How to get AI job in India"

col3, col4 = st.columns(2)
with col3:
    if st.button("What is RAG in AI"):
        st.session_state.topic = "What is RAG in AI"
with col4:
    if st.button("Best AI tools 2025"):
        st.session_state.topic = "Best AI tools 2025"

st.divider()

# Input
topic = st.text_input(
    "Enter research topic:",
    value=st.session_state.get("topic", ""),
    placeholder="e.g. Latest developments in Generative AI"
)

if st.button("🔍 Start Research", use_container_width=True):
    if topic:
        # Clear previous topic
        if "topic" in st.session_state:
            del st.session_state.topic

        # Show steps
        st.markdown("**Agent working...**")

        step1 = st.empty()
        step2 = st.empty()
        step3 = st.empty()

        step1.markdown('<div class="step-box">📡 Step 1: Searching the web...</div>', unsafe_allow_html=True)

        # Search
        try:
            search = GoogleSearch({
                "q": topic,
                "api_key": serpapi_key,
                "num": 5
            })
            results = search.get_dict()
            snippets = ""
            if "organic_results" in results:
                for r in results["organic_results"][:5]:
                    snippets += r.get("snippet", "") + "\n"

            step2.markdown('<div class="step-box">🧠 Step 2: Analyzing results with AI...</div>', unsafe_allow_html=True)

            # Ask Gemini
            prompt = f"""You are a research agent. Based on the search results below,
write a comprehensive and well structured summary about: {topic}

Search Results:
{snippets}

Write a clear detailed summary with key points. Use markdown formatting:"""

            data = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(url, json=data)
            result = response.json()

            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                answer = "API Error: " + str(result)

            step3.markdown('<div class="step-box">✅ Step 3: Research complete!</div>', unsafe_allow_html=True)

            # Show result
            st.divider()
            st.markdown(f"### Research Results: {topic}")
            st.markdown(answer)

            # Download button
            st.download_button(
                label="📥 Download Research",
                data=answer,
                file_name=f"research_{topic[:20]}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a topic!")