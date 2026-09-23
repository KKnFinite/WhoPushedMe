CREATE TABLE round_receipt_seen_state (
    round_id uuid NOT NULL,
    participant_id uuid NOT NULL,
    last_seen_event_id uuid REFERENCES round_events(id) ON DELETE SET NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (participant_id),
    FOREIGN KEY (participant_id, round_id)
        REFERENCES round_participants(id, round_id)
        ON DELETE CASCADE
);

CREATE INDEX round_receipt_seen_round_idx
    ON round_receipt_seen_state(round_id, updated_at DESC);
