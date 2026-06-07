import yt_dlp
import webvtt
import os
import sys

VIDEO_URL = "https://www.youtube.com/watch?v=8KkKuTCFvzI"
VTT_FILE = "raw.en.vtt"
OUTPUT_FILE = "PODCAST_SUMMARY.txt"
KEY_WORDS = ["important", "remember", "result", "goal", "finally", "because", "point"]


def create_summary(video_url=VIDEO_URL):
    try:
        print("🤖 STEP 1: Extracting transcript...")
        ydl_opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'outtmpl': 'raw',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        if not os.path.exists(VTT_FILE):
            print("❌ No English captions found for this video.")
            sys.exit(1)

        print("🤖 STEP 2: Summarizing Key Points...")
        summary_points = []

        for caption in webvtt.read(VTT_FILE):
            text = caption.text.strip()
            if any(word in text.lower() for word in KEY_WORDS):
                if text not in summary_points:
                    summary_points.append(text)

        print("🤖 STEP 3: Saving Summary...")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("--- KEY POINTS SUMMARY ---\n\n")
            for point in summary_points[:15]:
                f.write(f"• {point}\n")

        print(f"🏁 GOAL REACHED! Check '{OUTPUT_FILE}' for the key points.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up temp VTT file
        if os.path.exists(VTT_FILE):
            os.remove(VTT_FILE)


if __name__ == "__main__":
    create_summary()
