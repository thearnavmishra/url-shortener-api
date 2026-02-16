# URL Shortener API

A FastAPI-based URL shortener with click analytics and duplicate URL handling.

## Features

- Shorten long URLs
- Redirect using short code
- Click tracking and analytics
- Duplicate URL detection
- RESTful API design

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy

## Run Locally

```bash
py -m uvicorn main:app --reload
```

Open in browser:

http://127.0.0.1:8000/docs

## API Endpoints

- POST /shorten — Create short URL  
- GET /{code} — Redirect to original URL  
- GET /stats/{code} — Get click analytics
