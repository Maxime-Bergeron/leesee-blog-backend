# Leesee Blog — Backend API

Flask REST API using **Python**, **Flask-SQLAlchemy**, and **SQLAlchemy**. It stores articles in SQLite for local development and PostgreSQL on Render.

## Live deployment

- **Backend (Render):** https://leesee-blog-api.onrender.com
- **Health check:** https://leesee-blog-api.onrender.com/api/health
- **Posts API:** https://leesee-blog-api.onrender.com/api/posts
- **Frontend (Vercel):** https://leesee-blog-frontend-ten.vercel.app

## Requirements

- Python 3
- pip

## Run locally (Windows PowerShell)

From this backend repository's root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python seed.py
python app.py
```

The API will run at http://localhost:5000. If PowerShell blocks virtual-environment activation, you can run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry.

For macOS/Linux, activate the environment with `source .venv/bin/activate`.

By default, Flask-SQLAlchemy uses the local SQLite database `sqlite:///blog.db` when `DATABASE_URL` is unset. `seed.py` adds three example articles if they are not already present.

## Automated tests

```powershell
python -m pytest -q
```

Four tests cover API behavior, including article creation and validation. All four passed during local verification.

## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Basic server health response |
| GET | `/api/posts` | List articles, optionally filter with `?category=...` |
| GET | `/api/posts/<slug>` | Retrieve a single article |
| POST | `/api/posts` | Publish a new article |

Example POST JSON:

```json
{
  "title": "My first article",
  "slug": "my-first-article",
  "excerpt": "A short description",
  "content": "Article text goes here.",
  "category": "Technology"
}
```

## Deploy to Render

1. Create a Render PostgreSQL database and a Python web service connected to the [backend repository](https://github.com/Maxime-Bergeron/leesee-blog-backend).
2. Use these commands:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn app:app`
3. Set the following environment variables on the web service:
   - `DATABASE_URL`: your **private** PostgreSQL Internal Database URL from Render
   - `FRONTEND_URL`: `https://leesee-blog-frontend-ten.vercel.app`
4. Deploy and confirm `/api/health` returns `{"status":"ok"}` and `/api/posts` responds.
5. Publish an article from the Vercel frontend and check that it appears in `/api/posts` and remains after a refresh.

The application creates missing tables on startup using `db.create_all()`. A new PostgreSQL database starts with no demo posts. `seed.py` may be run against it if sample data is desired.

**Security note:** Publishing is intentionally public for this technical test; add authentication, authorization, and rate limiting before any production use. Never commit database credentials or environment files.
