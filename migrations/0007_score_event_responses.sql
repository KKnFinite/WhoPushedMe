ALTER TABLE round_events
    ADD COLUMN reply_to_event_id uuid
        REFERENCES round_events(id) ON DELETE CASCADE;

CREATE INDEX round_events_reply_to_idx
    ON round_events(reply_to_event_id, created_at, id)
    WHERE reply_to_event_id IS NOT NULL;
