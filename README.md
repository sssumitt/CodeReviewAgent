# Code Review Assistant

An AI-powered, self-hosted code review tool built with FastAPI and SQLite. Upload a file and get instant feedback on your code.

The app auto-creates `code_reviews.db` on first run.

---

## Features

* Upload a source file and get an actionable code review.
* Reports saved in a local SQLite database.
* Minimal dashboard at `/` with Markdown rendering and code highlighting.
* Supports multiple languages (Python, JS/TS, Java, C/C++, Go, Rust, Ruby).

---

## Prerequisites

* Python 3.10+
* Gemini (Google Generative AI) API key

---

## Install

```bash
uv venv
uv sync
```

---

## Configuration

Create a `.env` file with:

```
GEMINI_API_KEY=your_key_here
DATABASE_URL="sqlite:///./code_reviews.db"
```

---

## Run (development)

```bash
uv run -- uvicorn app.main:app --reload
```

Open browser at `http://localhost:8000` for the dashboard.

---

## API Endpoints

* `POST /review-file` — Upload a file.
* `GET /reports` — List recent reports.
* `GET /report/{uuid}` — Get specific report.
* `GET /` — Dashboard UI.

---

## Notes

* Database auto-created; no manual setup needed.
* Default model: `gemini-2.5-pro`.
* Large files may need chunking or background processing.
