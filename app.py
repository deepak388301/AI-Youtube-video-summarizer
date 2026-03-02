import streamlit as st
import yt_dlp
import requests
import webvtt
from io import StringIO
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import re

# Automatic data download for the cloud
nltk.download('punkt')
nltk.download('punkt_tab')

st.set_page_config(page_title="AI Podcast Pro", page_icon="📝", layout="wide")

# PROFESSIONAL CSS (The "AI Tool" Look)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { background: linear-gradient(to right, #6a11cb, #2575fc); color: white; border-radius: 12px; height: 3.5em; border: none; font-weight: bold; }
    .key-insight-card { background-color: white; padding: 24px; border-radius: 16px; border-left: 8px solid #6a11cb; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); font-family: 'Inter', sans-serif; line-height: 1.6; color: #2c3e50; }
    .tag { display: inline-block; background: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

def clean_text(text):
    # Remove repetitive stutters like "what we what we" or "uh uh"
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(uh|um|ah|so|like)\b', '', text, flags=re.IGNORECASE)
    return text.strip()

st.markdown("<h1 style='text-align: center;'>🎙️ AI Podcast Summary Pro</h1>", unsafe_allow_html=True)
url = st.text_input("YouTube URL:", placeholder="Paste your podcast link here...")

if st.button("✨ Generate Professional Insights"):
    try:
        with st.spinner("🧠 AI is polishing the transcript..."):
            ydl_opts = {'skip_download': True, 'writeautomaticsub': True, 'subtitleslangs': ['en'], 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                subs_url = info.get('requested_subtitles', {}).get('en', {}).get('url')
                
                if subs_url:
                    r = requests.get(subs_url)
                    vtt_content = StringIO(r.text)
                    raw_lines = [c.text.strip() for c in webvtt.read_buffer(vtt_content)]
                    
                    # CLEANING PHASE
                    cleaned_body = clean_text(" ".join(raw_lines))
                    
                    # SUMMARIZATION PHASE
                    parser = PlaintextParser.from_string(cleaned_body, Tokenizer("english"))
                    summarizer = LuhnSummarizer()
                    summary = summarizer(parser.document, 5) # 5 High-Value Points

                    st.markdown("### 🚀 Executive Summary")
                    for sentence in summary:
                        st.markdown(f"""
                            <div class="key-insight-card">
                                <span class="tag">KEY TAKEAWAY</span><br>
                                {sentence}
                            </div>
                            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")