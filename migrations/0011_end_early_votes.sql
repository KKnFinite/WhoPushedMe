CREATE TABLE round_end_early_votes (
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    participant_id uuid NOT NULL,
    vote boolean NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, participant_id),
    FOREIGN KEY (participant_id, round_id)
        REFERENCES round_participants(id, round_id)
        ON DELETE CASCADE
);

CREATE INDEX round_end_early_votes_updated_idx
    ON round_end_early_votes(round_id, updated_at DESC);
