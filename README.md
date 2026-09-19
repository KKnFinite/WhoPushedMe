# Who Pushed Me?! Scorecard

A mobile-first golf scorecard prototype built around fast scoring, shared rounds, score-change receipts, and aggressively unnecessary trash talk.

## Prototype 0.3

Current foundation:

- Flask web app
- Render deployment
- Neon Postgres-backed schema and versioned migrations
- Username/password accounts with hashed no-email recovery keys and bearer sessions
- Temporary compatibility for legacy anonymous recovery-key identities
- Individual and Scramble round data services
- Score/par receipts and a generic round-event ledger
- Optional Scramble contribution records
- OpenGolfAPI course-cache adapter
- `/health` endpoint
- Mobile-first UI

The existing Home buttons remain intentionally parked while the backend API settles.

Planned next:

- Finish the real account/login UI
- Wire the Home flow to the round API
- Add live round synchronization
- Expand event-specific trash-talk content

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

The real account flow uses:

- `POST /api/auth/register` with username, password, and display name
- `POST /api/auth/login`
- `POST /api/auth/recover` with the one-time recovery key and a new password
- `GET /api/auth/me`
- `POST /api/auth/logout`

Passwords, recovery keys, and session tokens are stored only as hashes. Registration
returns the recovery key once. A successful recovery rotates that key, revokes older
sessions, and returns the replacement key once.

Authenticated round requests accept `Authorization: Bearer <session-token>`.
Legacy `X-Recovery-Key` authentication remains temporarily supported while the UI
and old prototype identity flow are migrated.

The round API supports creating/joining rounds, reading shared state, changing the
shared current hole and lifecycle, recording pars/scores, editing Scramble
contributions, and posting role-limited social events.

## Environment

`DATABASE_URL` is intentionally never committed. Local Neon project linkage lives in `.neon`, which is also ignored.
