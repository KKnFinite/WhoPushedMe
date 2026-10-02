CREATE INDEX IF NOT EXISTS rounds_unfinished_updated_idx
    ON rounds(updated_at)
    WHERE status IN ('setup', 'active');
