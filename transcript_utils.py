import yt_dlp
import json
import os
import re


def clean_transcript(text: str):
    text = re.sub(r"\[.*?\]", "", text)   # remove [Music]
    text = re.sub(r"\s+", " ", text)      # fix spacing
    return text.strip()


def fetch_transcript_with_ytdlp(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_path = f"temp_{video_id}"

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'json3',
        'outtmpl': output_path,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file_path = f"{output_path}.en.json3"

        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        transcript = []
        for event in data.get("events", []):
            if "segs" in event:
                for seg in event["segs"]:
                    transcript.append(seg.get("utf8", ""))

        os.remove(file_path)

        final_text = " ".join(transcript)
        return clean_transcript(final_text)

    except Exception:
        return None