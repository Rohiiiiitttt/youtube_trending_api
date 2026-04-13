from fastapi import FastAPI, Query
import requests
from youtube_transcript_api import YouTubeTranscriptApi

from transcript_utils import fetch_transcript_with_ytdlp, clean_transcript

app = FastAPI()

YOUTUBE_API_URL = "http://127.0.0.1:8000/recommend"


@app.get("/")
def root():
    return {"message": "Transcription API running"}


@app.get("/transcribe")
def transcribe(topic: str = Query(...)):

    try:
        res = requests.get(YOUTUBE_API_URL, params={"topic": topic, "max_results": 5})
        data = res.json()
    except Exception as e:
        return {"error": f"YouTube API failed: {str(e)}"}

    videos = data.get("results", [])

    for video in videos:
        video_id = video["video_id"]
        title = video["title"]
        url = video["url"]

        # 🔥 NEW FIXED METHOD
        try:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id)

            text = " ".join([item.text for item in transcript])
            text = clean_transcript(text)

            return {
                "title": title,
                "video_url": url,
                "source": "youtube_transcript_api",
                "transcript": text
            }

        except Exception:
            pass

        # 🔁 fallback
        text = fetch_transcript_with_ytdlp(video_id)

        if text:
            return {
                "title": title,
                "video_url": url,
                "source": "yt-dlp",
                "transcript": text
            }

    return {
        "error": "No transcript found for any video"
    }