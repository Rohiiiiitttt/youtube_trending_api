# 🚀 VidScribe AI

VidScribe AI is a **microservices-based system** that intelligently fetches, ranks, and transcribes YouTube videos.
It ensures high-quality transcript extraction even when subtitles are not directly available.

---

## 🧠 Overview

This project is designed to:

* 🔍 Fetch YouTube videos based on a topic
* 📊 Rank videos using a custom scoring algorithm
* 🎯 Select the most relevant video
* 📝 Generate transcripts using multiple fallback methods

---

## 🏗️ Architecture

```
User Request
     ↓
youtube_api (Fetch + Rank Videos)
     ↓
transcript_api (Select + Transcribe)
     ↓
JSON Response
```

---

## 📁 Project Structure

```
VidScribe-AI/
│
├── youtube_api/
│   ├── main.py
│   └── requirements.txt
│
├── transcript_api/
│   ├── main.py
│   ├── transcript_utils.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd VidScribe-AI
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```
cd youtube_api
pip install -r requirements.txt

cd ../transcript_api
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file inside `youtube_api/`:

```
YOUTUBE_API_KEY=your_api_key_here
```

---

## ▶️ Running the Project

### Terminal 1 (YouTube API)

```
cd youtube_api
uvicorn main:app --port 8000
```

---

### Terminal 2 (Transcription API)

```
cd transcript_api
uvicorn main:app --port 8001
```

---

## 🌐 API Endpoints

### 🔹 Get Ranked Videos

```
GET /recommend?topic=python
```

---

### 🔹 Get Transcript

```
GET /transcribe?topic=python
```

---

## ⚡ Features

* 📊 **Custom Ranking Algorithm**

  * Based on likes, comments, views, and recency

* 🔁 **Smart Fallback Mechanism**

  * Uses youtube-transcript-api
  * Falls back to yt-dlp if needed

* 🧠 **Intelligent Video Selection**

  * Chooses best video dynamically

* ⚙️ **Microservices Architecture**

  * Separate APIs for scalability

---

## 🛠️ Tech Stack

* FastAPI
* YouTube Data API v3
* youtube-transcript-api
* yt-dlp
* Python

---

## 🎯 Example Output

```json
{
  "title": "Python Full Course for Beginners",
  "video_url": "https://www.youtube.com/watch?v=...",
  "source": "youtube_transcript_api",
  "transcript": "..."
}
```

---

## 📌 Future Improvements

* 🧠 LLM-based summarization
* ⏱ Timestamp segmentation
* 🌐 Frontend UI integration
* ☁️ Deployment (Docker / Cloud)

---

## 👨‍💻 Author

Developed as part of a production-style backend system for intelligent video content processing.

