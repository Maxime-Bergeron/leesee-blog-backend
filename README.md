# Leesee Blog API

Flask REST API with SQLAlchemy. SQLite for local development; PostgreSQL recommended in production.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

API: http://localhost:5000/api/posts

## Tests

```bash
pytest -q
```

## Endpoints

- `GET /api/health`
- `GET /api/posts` (optional `?category=...`)
- `GET /api/posts/<slug>`
- `POST /api/posts` (JSON with title, slug, excerpt, content, category)

## Deploy to Render

1. Create a public GitHub repository and push the contents of this backend directory.
2. Create a managed PostgreSQL database and copy its **internal** connection URL.
3. Create a Render Web Service connected to the backend repository (or use `render.yaml`).
4. Build command: `pip install -r requirements.txt`; start command: `gunicorn app:app`.
5. Set `DATABASE_URL` to the PostgreSQL URL and `FRONTEND_URL` to the Vercel deployment URL.
6. Deploy and verify `/api/health` returns `{"status":"ok"}`.
7. Optional seed: run `python seed.py` against the production database using a secure shell.

**Security note:** Article creation is public for demonstration purposes. Add authentication and rate limiting before using in production.

## Live URLs

Backend: _Add your deployed Render URL here._
Frontend: _Add your deployed Vercel URL here._
