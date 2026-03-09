from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from datetime import datetime, timezone
from dateutil import parser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Check .env file.")

youtube = build("youtube", "v3", developerKey=API_KEY)

app = FastAPI()

# ------------------- CORS -------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------


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

            # Filter only educational videos
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
                "channel": video["snippet"]["channelTitle"],
                "views": views,
                "likes": likes,
                "comments": comments,
                "score": score,
                "published_date": published,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    if sorted_results:
        max_score = sorted_results[0]["score"]

        for video in sorted_results:
            percentage_score = (video["score"] / max_score) * 100 if max_score > 0 else 0
            video["score_percentage"] = round(percentage_score, 2)
            video["score"] = round(video["score"], 6)

    for idx, video in enumerate(sorted_results, start=1):
        video["rank"] = idx

    return sorted_results


@app.get("/")
def root():
    return {"message": "YouTube Course Recommender API is running"}


@app.get("/recommend")
def recommend_videos(
    topic: str = Query(..., description="Topic to search"),
    max_results: int = Query(11, ge=1, le=50, description="Number of videos to fetch (1–50)")
):

    videos = fetch_videos(topic, max_results)

    return {
        "topic": topic,
        "total_results_returned": len(videos),
        "results": videos
    }