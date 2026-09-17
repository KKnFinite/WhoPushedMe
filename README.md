# Who Pushed Me?! Scorecard

A mobile-first golf scorecard prototype built around fast scoring, shared rounds, score-change receipts, and aggressively unnecessary trash talk.

## Prototype 0.3

Current foundation:

- Flask web app
- Render deployment
- Neon Postgres-backed schema and versioned migrations
- Anonymous golfer identities with recovery keys
- Individual and Scramble round data services
- Score/par receipts and a generic round-event ledger
- Optional Scramble contribution records
- OpenGolfAPI course-cache adapter
- `/health` endpoint
- Mobile-first UI

The existing Home buttons remain intentionally parked while the backend API settles.

Planned next:

- Wire the Home flow to the round API
- Add live round synchronization
- Server-selected trash talk events
- Large anti-repetition trash-talk bank

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Database migrations

Migrations prefer `DATABASE_URL_UNPOOLED` and fall back to `DATABASE_URL`:

```powershell
python -m migrations
```

The first migration creates golfers, shared rounds and participants, hole pars and
scores, the generic event ledger, optional Scramble contributions, and normalized
OpenGolfAPI cache tables. Free Play rounds leave `course_id` empty.

## Backend API

Create or recover an anonymous golfer through `/api/golfers`, then send the returned
recovery key as `X-Recovery-Key` for round requests under `/api/rounds`. The API
supports creating/joining rounds, reading shared state, changing the shared current
hole and lifecycle, recording pars/scores, editing Scramble contributions, and
posting role-limited social events. It is intentionally not wired to the Home UI yet.

## Environment

`DATABASE_URL` is intentionally never committed. Local Neon project linkage lives in `.neon`, which is also ignored.
