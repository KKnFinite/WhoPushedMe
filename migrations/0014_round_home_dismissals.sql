CREATE TABLE round_home_dismissals (
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    golfer_id uuid NOT NULL REFERENCES golfers(id) ON DELETE CASCADE,
    dismissed_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, golfer_id)
);

CREATE INDEX round_home_dismissals_golfer_idx
    ON round_home_dismissals(golfer_id, dismissed_at DESC);
