CREATE TABLE round_history_access (
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    golfer_id uuid NOT NULL REFERENCES golfers(id) ON DELETE CASCADE,
    participant_id uuid NOT NULL REFERENCES round_participants(id) ON DELETE CASCADE,
    reason text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, golfer_id, participant_id)
);

CREATE INDEX round_history_access_golfer_idx
    ON round_history_access(golfer_id, created_at DESC);
