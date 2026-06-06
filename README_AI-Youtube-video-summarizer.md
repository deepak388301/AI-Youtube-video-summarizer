# 🎙️ AI YouTube Video Summarizer

A web app that extracts and summarizes YouTube video transcripts using NLP, surfacing the most important insights from long-form content in seconds.

---

## What It Does

Paste any YouTube URL and the app fetches the video's auto-generated captions, cleans the raw transcript (removing filler words and stutters), then runs an NLP summarization algorithm to surface the top key takeaways — presented as a clean, card-based dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Transcript Extraction | `yt-dlp`, `webvtt-py` |
| NLP Summarization | `sumy` (Luhn algorithm) |
| Text Cleaning | `nltk`, `re` |
| Backend | Python |

---

## Features

- Fetches auto-generated captions from any YouTube video via `yt-dlp`
- Cleans raw transcript: removes repeated words, filler phrases (uh, um, ah)
- Applies Luhn NLP summarization to extract the 5 highest-value sentences
- Displays results as styled "Key Takeaway" cards in a professional UI
- Works on podcasts, lectures, interviews, and any caption-enabled video

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/deepak388301/AI-Youtube-video-summarizer.git
cd AI-Youtube-video-summarizer
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser, paste a YouTube URL, and click **Generate Professional Insights**.

---

## How It Works

1. `yt-dlp` fetches the video's English subtitle URL without downloading the video
2. The `.vtt` subtitle file is streamed and parsed with `webvtt`
3. Raw caption text is cleaned — duplicate words and filler phrases are stripped using regex
4. `sumy`'s `LuhnSummarizer` scores sentences by keyword frequency and extracts the top 5
5. Results are rendered in Streamlit with custom CSS styling

---

## Project Structure

```
AI-Youtube-video-summarizer/
├── app.py                 # Main Streamlit application
├── podcast_bot.py         # Alternate summarization module
├── requirements.txt       # Python dependencies
└── .gitignore.txt         # Files excluded from version control
```

> **Note:** The `node_modules`-equivalent dependency folders currently committed to the repo root should be removed. Add a proper `.gitignore` to exclude installed packages.

---

## Future Improvements

- Add support for multiple summary lengths (brief / detailed)
- Support manual transcript paste for videos without captions
- Export summary as PDF or Markdown
- Add language selection for non-English videos

---

## Author

**Deepak E** — ECE Undergrad | Web & AI Developer  
[LinkedIn](https://www.linkedin.com/in/deepak-e-3a3485330) · [GitHub](https://github.com/deepak388301)
