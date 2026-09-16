# Who Pushed Me?! Scorecard

A mobile-first golf scorecard prototype built around fast scoring, shared rounds, score-change receipts, and aggressively unnecessary trash talk.

## Prototype 0.1

Current foundation:

- Flask web app
- Render deployment
- Neon Postgres-ready configuration
- Individual and Scramble setup flows
- `/health` endpoint
- Mobile-first UI

Planned next:

- Persisted rounds and players
- Hole-by-hole scoring
- Shared live Scramble updates
- Server-selected trash talk events
- Score audit history ("Who Pushed Me?!")
- Large anti-repetition trash-talk bank

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Environment

`DATABASE_URL` is intentionally never committed. Local Neon project linkage lives in `.neon`, which is also ignored.
