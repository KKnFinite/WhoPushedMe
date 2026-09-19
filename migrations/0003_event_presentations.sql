ALTER TABLE round_events
    ADD COLUMN content_event_key text,
    ADD COLUMN presentation jsonb NOT NULL DEFAULT '{}'::jsonb;

CREATE INDEX round_events_content_event_idx
    ON round_events(content_event_key)
    WHERE content_event_key IS NOT NULL;
