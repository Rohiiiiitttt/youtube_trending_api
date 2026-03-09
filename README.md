# YouTube Trending API

This project is a FastAPI backend service that recommends educational YouTube videos based on a given topic.

It uses the YouTube Data API to fetch videos and ranks them based on engagement metrics such as views, likes, comments, and recency.

## Technologies Used

- Python
- FastAPI
- YouTube Data API
- Uvicorn
- python-dotenv

## Installation

1. Clone the repository

git clone <repo-link>

2. Navigate to the project folder

cd youtube_trending_api

3. Create virtual environment

python -m venv venv

4. Activate virtual environment

Windows:
venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

## Environment Variables

Create a `.env` file and add:

YOUTUBE_API_KEY=your_api_key_here

## Run the API

uvicorn main:app --reload

API will run at:

http://127.0.0.1:8000

## API Endpoint

GET /recommend?topic=python lists

Returns ranked YouTube videos related to the topic.