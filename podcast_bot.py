import yt_dlp
import webvtt

video_url = "https://www.youtube.com/watch?v=8KkKuTCFvzI"

def create_summary():
    try:
        print("🤖 STEP 1: Extracting transcript...")
        ydl_opts = {'skip_download': True, 'writeautomaticsub': True, 'subtitleslangs': ['en'], 'outtmpl': 'raw'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("🤖 STEP 2: Summarizing Key Points...")
        # These are the words your bot will look for to find 'Important' parts
        key_words = ["important", "remember", "result", "goal", "finally", "because", "point"]
        summary_points = []

        for caption in webvtt.read('raw.en.vtt'):
            text = caption.text.strip()
            # Only keep the sentence if it has a Key Word and isn't a duplicate
            if any(word in text.lower() for word in key_words):
                if text not in summary_points:
                    summary_points.append(text)

        print("🤖 STEP 3: Saving Summary...")
        with open("PODCAST_SUMMARY.txt", "w", encoding="utf-8") as f:
            f.write("--- KEY POINTS SUMMARY ---\n\n")
            for point in summary_points[:15]: # Limit to top 15 key points
                f.write(f"• {point}\n")
            
        print("🏁 GOAL REACHED! Check 'PODCAST_SUMMARY.txt' for the key points.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_summary()