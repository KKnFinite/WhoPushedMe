ALTER TABLE golfers
    ADD COLUMN username varchar(24),
    ADD COLUMN password_hash text,
    ADD COLUMN recovery_key_hash char(64),
    ADD COLUMN is_admin boolean NOT NULL DEFAULT false;

ALTER TABLE golfers
    ALTER COLUMN recovery_key DROP NOT NULL;

CREATE UNIQUE INDEX golfers_username_lower_unique
    ON golfers (lower(username))
    WHERE username IS NOT NULL;

CREATE UNIQUE INDEX golfers_recovery_key_hash_unique
    ON golfers (recovery_key_hash)
    WHERE recovery_key_hash IS NOT NULL;

CREATE TABLE auth_sessions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    golfer_id uuid NOT NULL REFERENCES golfers(id) ON DELETE CASCADE,
    token_hash char(64) NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now(),
    expires_at timestamptz NOT NULL,
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    revoked_at timestamptz,
    CHECK (expires_at > created_at)
);

CREATE INDEX auth_sessions_active_golfer_idx
    ON auth_sessions(golfer_id, expires_at)
    WHERE revoked_at IS NULL;
