# 🎬 YouTube Course Recommender & Transcript API

A FastAPI backend that recommends high-quality educational YouTube videos and provides transcripts for any video.

---

## 🚀 Features

* 🔍 Search YouTube videos by topic
* 🎯 Smart ranking using:

  * Views
  * Likes
  * Comments
  * Recency
* 📚 Filters educational videos (Category 27)
* 🧠 Transcript extraction:

  * Primary: `youtube-transcript-api`
  * Fallback: `yt-dlp`
* 📄 Returns transcript as text
* ⚡ FastAPI with interactive API docs

---

## 🏗️ Project Structure

```
project/
│── main.py
│── transcript_utils.py
│── requirements.txt
│── .env
```

---

## ⚙️ Tech Stack

* Python
* FastAPI
* YouTube Data API v3
* youtube-transcript-api
* yt-dlp

---

## 🔑 Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add your API key

Create a `.env` file:

```
YOUTUBE_API_KEY=your_api_key_here
```

---

## ▶️ Run the Server

```
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 🔹 GET `/recommend`

Returns ranked educational videos based on engagement and recency.

**Query Parameters:**

* `topic` (string) — required
* `max_results` (int) — default: 5

---

### 🔹 GET `/transcript`

Returns transcript of a YouTube video.

**Query Parameters:**

* `video_id` (string) — required

---

## 📦 Sample Response

```
{
  "video_id": "abc123",
  "source": "youtube_transcript_api",
  "transcript": "This is the full transcript text of the video..."
}
```

---

## ⚠️ Notes

* Some videos may not have transcripts available
* Fallback using `yt-dlp` improves success rate
* `.env` file is not included for security reasons

---

## 🌟 Future Improvements

* Structured JSON transcript
* AI-based summarization
* Keyword extraction
* Frontend integration

---

## 👨‍💻 Author

Rohit Ghodake

---

## 📄 License

This project is for educational purposes.
