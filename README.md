# Code Review Assistant

Single-file FastAPI application that accepts source code file uploads, calls the Gemini 2.5 Pro API to analyze code and produce a review report, stores reports in a SQLite database, and provides a small dashboard for uploading files and viewing reports.

This repository contains a single main application file (e.g. `code_review_assistant.py`). The app automatically creates a SQLite database file (`code_reviews.db`) on first run.

---

## Features

* Upload a single source file and receive a concise, actionable code review powered by Gemini 2.5 Pro.
* Reports persisted in a local SQLite database using `sqlmodel`.
* Minimal, modern dashboard (served at `/`) that renders review content as Markdown and highlights source code.
* Supports multiple languages by filename heuristic (Python, JS/TS, Java, C/C++, Go, Rust, Ruby).

---

## Prerequisites

* Python 3.10 or newer
* A Gemini (Google Generative AI) API key

---

## Install

```bash
uv init
uv venv
uv sync
---

## Run (development)

Start the FastAPI server with uvicorn:

```bash
uv run -- uvicorn app.main:app --reload
```

Open your browser to:

```
http://localhost:8000
```

The dashboard will let you upload a file for review and view previously generated reports.

---

## HTTP API Endpoints

* `POST /review-file` — Upload a single source file. Expects multipart form with field `file` and optional form field `model`.

  * Example `curl`:

```bash
curl -F "file=@example.py" http://localhost:8000/review-file
```

* `GET /reports` — List recent reports (JSON).

```bash
curl http://localhost:8000/reports
```

* `GET /report/{uuid}` — Fetch a specific report (code + review text).

```bash
curl http://localhost:8000/report/<REPORT_UUID>
```

* `GET /` — Dashboard UI (renders Markdown and highlights code).

---

## Notes

* The SQLite database file `code_reviews.db` is created automatically on first run. You do not need to initialize it manually.
* The default model used by the app is `gemini-2.5-pro`. The request body allows specifying a different model name when calling `/review-file`.
* For large codebases or many files, consider zipping files and implementing chunked analysis or a background worker and queue.

---

## Troubleshooting

* If the dashboard or server cannot find installed packages (for example, `aiofiles`), ensure you are running the server with the same Python interpreter/environment where you installed the packages.

```bash
# check which python is used
which python
# or
python -m pip show aiofiles
```

* If you see a warning that `GEMINI_API_KEY` is not set, confirm the `.env` file is present and that the application has been restarted after creating `.env`.

* On Windows, if you set environment variables with `setx`, you must open a new terminal to pick them up. Using `.env` and `python-dotenv` avoids this.

---

## Security and production considerations

* Do not commit secrets to source control. Use a secrets manager for production.
* Add authentication to the API and dashboard before exposing to public networks.
* Add rate limiting and request size limits to protect against abuse.
* For production, consider running with a process manager (systemd, docker-compose, k8s) and a more robust database.

---

## Optional improvements

* Multi-file / zip upload handling and cross-file analysis.
* Background job queue for long-running reviews (Redis + RQ/Celery/FastAPI background tasks).
* Structured review JSON (separate fields for bugs/security/performance) for richer UI features.
* Add unit tests and CI for automated checks.

---

## License

This project is provided as-is. Add a license file as appropriate for your use.
