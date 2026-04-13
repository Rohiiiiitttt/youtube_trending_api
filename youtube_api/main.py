from fastapi import FastAPI, Query
from googleapiclient.discovery import build
from datetime import datetime, timezone
from dateutil import parser
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Check .env file.")

youtube = build("youtube", "v3", developerKey=API_KEY)

app = FastAPI()


def fetch_videos(topic: str, max_results: int):
    search_request = youtube.search().list(
        q=topic,
        part="snippet",
        type="video",
        videoDuration="long",
        maxResults=max_results
    )

    search_response = search_request.execute()
    results = []

    for item in search_response["items"]:
        video_id = item["id"]["videoId"]

        video_request = youtube.videos().list(
            part="statistics,snippet",
            id=video_id
        )

        video_response = video_request.execute()

        for video in video_response["items"]:
            if video["snippet"].get("categoryId") != "27":
                continue

            views = int(video["statistics"].get("viewCount", 0))
            likes = int(video["statistics"].get("likeCount", 0))
            comments = int(video["statistics"].get("commentCount", 0))

            if views < 1000:
                continue

            published = video["snippet"]["publishedAt"]
            publish_date = parser.parse(published)

            days_old = (datetime.now(timezone.utc) - publish_date).days
            recency_factor = 1 / ((days_old + 1) ** 0.2)

            like_ratio = likes / views if views else 0
            comment_ratio = comments / views if views else 0

            score = ((like_ratio * 0.6) + (comment_ratio * 0.3)) * recency_factor

            results.append({
                "title": video["snippet"]["title"],
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "score": score
            })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    for idx, video in enumerate(sorted_results, start=1):
        video["rank"] = idx
        video["score"] = round(video["score"], 6)

    return sorted_results


@app.get("/")
def root():
    return {"message": "YouTube API running"}


@app.get("/recommend")
def recommend_videos(topic: str = Query(...), max_results: int = 5):
    videos = fetch_videos(topic, max_results)

    return {
        "topic": topic,
        "results": videos
    }