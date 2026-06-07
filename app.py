import streamlit as st
import yt_dlp
import requests
import webvtt
import tempfile
import os
import nltk
import re
from io import StringIO
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

# Download only if not already present
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

st.set_page_config(page_title="AI Podcast Pro", page_icon="📝", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { background: linear-gradient(to right, #6a11cb, #2575fc); color: white; border-radius: 12px; height: 3.5em; border: none; font-weight: bold; }
    .key-insight-card { background-color: white; padding: 24px; border-radius: 16px; border-left: 8px solid #6a11cb; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); font-family: 'Inter', sans-serif; line-height: 1.6; color: #2c3e50; }
    .tag { display: inline-block; background: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)


def clean_text(text):
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(uh|um|ah|so|like)\b', '', text, flags=re.IGNORECASE)
    return text.strip()


def fetch_transcript(url):
    """Fetch VTT subtitle content from a YouTube URL. Returns raw text or None."""
    ydl_opts = {
        'skip_download': True,
        'writeautomaticsub': True,
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Try requested_subtitles first (manual captions)
    subs_url = (
        (info.get('requested_subtitles') or {})
        .get('en', {})
        .get('url')
    )

    # Fall back to automatic_captions (auto-generated)
    if not subs_url:
        auto_caps = info.get('automatic_captions') or {}
        en_formats = auto_caps.get('en') or []
        # Prefer vtt format
        for fmt in en_formats:
            if fmt.get('ext') == 'vtt':
                subs_url = fmt.get('url')
                break
        # Take first available if no vtt found
        if not subs_url and en_formats:
            subs_url = en_formats[0].get('url')

    if not subs_url:
        return None

    r = requests.get(subs_url, timeout=15)
    r.raise_for_status()
    return r.text


def parse_vtt(vtt_text):
    """Parse VTT content string into a list of caption lines using a temp file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False, encoding='utf-8') as tmp:
        tmp.write(vtt_text)
        tmp_path = tmp.name

    try:
        lines = [c.text.strip() for c in webvtt.read(tmp_path)]
    finally:
        os.unlink(tmp_path)

    return lines


st.markdown("<h1 style='text-align: center;'>🎙️ AI Podcast Summary Pro</h1>", unsafe_allow_html=True)
url = st.text_input("YouTube URL:", placeholder="Paste your podcast link here...")

if st.button("✨ Generate Professional Insights"):
    if not url.strip():
        st.warning("Please enter a YouTube URL first.")
    else:
        try:
            with st.spinner("🧠 AI is polishing the transcript..."):
                vtt_text = fetch_transcript(url)

                if not vtt_text:
                    st.warning("No English captions found for this video. Try a video with auto-generated subtitles enabled.")
                else:
                    raw_lines = parse_vtt(vtt_text)
                    cleaned_body = clean_text(" ".join(raw_lines))

                    if not cleaned_body:
                        st.warning("Transcript was empty after cleaning. Nothing to summarize.")
                    else:
                        parser = PlaintextParser.from_string(cleaned_body, Tokenizer("english"))
                        summarizer = LuhnSummarizer()
                        summary = summarizer(parser.document, 5)

                        st.markdown("### 🚀 Executive Summary")
                        for sentence in summary:
                            st.markdown(f"""
                                <div class="key-insight-card">
                                    <span class="tag">KEY TAKEAWAY</span><br>
                                    {sentence}
                                </div>
                                """, unsafe_allow_html=True)

        except requests.HTTPError as e:
            st.error(f"Failed to fetch subtitles: {e}")
        except Exception as e:
            st.error(f"Error: {e}")
